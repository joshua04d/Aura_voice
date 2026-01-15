from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":prompt}],
        max_tokens=100
    )

    return response.choices[0].message.content
