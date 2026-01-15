conversation = []

def add_message(role, text):
    conversation.append({"role": role, "text": text})
    if len(conversation) > 10:
        conversation.pop(0)

def get_context():
    return conversation
