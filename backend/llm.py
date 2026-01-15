import requests

def get_copilot_suggestion(user_text, intent, context):
    prompt = f"""
You are AuraVoice, an AI copilot for insurance call agents.

Conversation context:
{context}

Customer just said:
{user_text}

Detected intent: {intent}

Suggest what the agent should say next.
Keep it short, friendly, and professional.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
