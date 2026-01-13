from fastapi import FastAPI, WebSocket
from faster_whisper import WhisperModel
import asyncio
import tempfile
import os

app = FastAPI()
model = WhisperModel("base", compute_type="int8")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    
    audio_buffer = bytearray()

    while True:
        data = await ws.receive_bytes()
        audio_buffer.extend(data)

        # Every ~2 seconds of audio → transcribe
        if len(audio_buffer) > 32000 * 2:  
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_buffer)
                temp_name = f.name

            segments, _ = model.transcribe(temp_name)
            text = " ".join([seg.text for seg in segments])

            await ws.send_text(text)

            audio_buffer = bytearray()
            os.remove(temp_name)
