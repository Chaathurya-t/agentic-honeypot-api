SCAM_SIGNALS = [
    "urgent", "blocked", "verify", "otp",
    "account", "upi", "bank", "click", "link",
    "suspended", "immediately", "payment"
]

def update_scam_score(message: str, state: dict):
    msg = message.lower()
    for word in SCAM_SIGNALS:
        if word in msg:
            state["scam_score"] += 1

    # Scam detected only after confidence threshold
    if state["scam_score"] >= 2:
        return True
    return False
