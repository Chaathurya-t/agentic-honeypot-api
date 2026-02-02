def update_scam_score(message: str, history: list) -> float:
    msg = message.lower()
    score = 0.0

    scam_keywords = [
        "urgent", "blocked", "verify", "pay", "payment",
        "upi", "bank", "account", "transfer", "click", "link"
    ]

    for word in scam_keywords:
        if word in msg:
            score += 0.15

    return min(score, 1.0)
