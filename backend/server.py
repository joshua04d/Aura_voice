from fastapi import FastAPI, WebSocket
from faster_whisper import WhisperModel
import tempfile, os

from memory import add_message, get_context
from intent import detect_intent
from llm import get_copilot_suggestion

app = FastAPI()
model = WhisperModel("base", compute_type="int8")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    audio_buffer = bytearray()

    while True:
        data = await ws.receive_bytes()
        audio_buffer.extend(data)

        if len(audio_buffer) > 32000 * 2:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_buffer)
                temp_name = f.name

            segments, _ = model.transcribe(temp_name)
            user_text = " ".join([seg.text for seg in segments]).strip()

            if user_text:
                add_message("customer", user_text)

                intent = detect_intent(user_text)
                context = get_context()

                suggestion = get_copilot_suggestion(user_text, intent, context)

                await ws.send_text(f"Customer: {user_text}")
                await ws.send_text(f"Copilot: {suggestion}")

                add_message("copilot", suggestion)

            audio_buffer = bytearray()
            os.remove(temp_name)
