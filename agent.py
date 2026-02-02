import random

def generate_agent_reply(message: str, history: list, scam_score: float) -> str:
    """
    Aggressive honeypot agent that extracts scam intelligence
    once scam intent is detected.
    """

    message_lower = message.lower()

    prompts = []

    # 🔥 Force aggressive behavior once scam is detected
    if any(word in message_lower for word in ["pay", "payment", "upi", "transfer"]):
        prompts.extend([
            "Okay, just a second… Please send your UPI ID clearly.",
            "I’m ready to pay. Can you confirm the UPI ID and account name?",
            "Before I pay, which bank is this UPI linked to?"
        ])

    if any(word in message_lower for word in ["bank", "account", "blocked"]):
        prompts.extend([
            "My app is asking for your bank name and account number.",
            "Can you confirm the account number again?",
            "Which bank branch is this account from?"
        ])

    if any(word in message_lower for word in ["link", "click", "verify"]):
        prompts.extend([
            "The link is not opening. Can you resend the full link?",
            "My browser is blocking this. Can you confirm the official link?",
            "Is this the correct verification link?"
        ])

    # Fallback if no keyword matched
    if not prompts:
        prompts = [
            "Please guide me step by step so I don’t make a mistake.",
            "I’m trying now. Can you confirm the payment details again?",
            "What exactly should I do next?"
        ]

    human_prefix = random.choice([
        "Okay…",
        "Wait a second…",
        "Hmm…",
        "Alright…"
    ])

    return f"{human_prefix} {random.choice(prompts)}"
