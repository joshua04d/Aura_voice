def detect_intent(text):
    text = text.lower()

    if "travel" in text:
        return "travel_insurance"
    if "car" in text or "vehicle" in text:
        return "car_insurance"
    if "health" in text or "medical" in text:
        return "health_insurance"

    return "general_query"
