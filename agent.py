import random

def generate_agent_reply(message: str, history: list, scam_score: float) -> str:
    """
    Generates a socially engineered agent reply
    that encourages scammers to reveal intelligence
    such as UPI IDs, bank details, and phishing links.
    """

    message_lower = message.lower()

    # If scam confidence is low → act like a normal confused user
    if scam_score < 0.5:
        return "Sorry, I’m not sure I understand. Could you explain again?"

    # If scam detected → aggressive but believable extraction
    prompts = []

    # Payment / UPI extraction
    if any(word in message_lower for word in ["pay", "payment", "upi", "transfer"]):
        prompts.extend([
            "Okay, I can pay. Please send your **UPI ID** clearly.",
            "I’m ready to transfer the amount. Can you confirm the **UPI ID** and **account name**?",
            "Before I pay, please confirm which **bank** this UPI is linked to."
        ])

    # Bank account extraction
    if any(word in message_lower for word in ["bank", "account", "blocked"]):
        prompts.extend([
            "My bank app is asking for your **account number** and **bank name**. Can you share that?",
            "Can you confirm the **bank name and account number** so I can proceed?",
            "The app shows an error. Please recheck and send your **account details**."
        ])

    # Phishing link extraction
    if any(word in message_lower for word in ["link", "click", "verify", "update"]):
        prompts.extend([
            "The link isn’t opening properly. Can you resend the **full link**?",
            "Is this link official? Please confirm before I click it again.",
            "My browser shows a warning. Can you confirm this **verification link** is safe?"
        ])

    # If nothing matched, still push gently
    if not prompts:
        prompts = [
            "I want to fix this quickly. What are the **exact steps** I need to follow?",
            "Please guide me step by step so I don’t make a mistake.",
            "Can you confirm the **payment details** again?"
        ]

    # Add human hesitation for realism
    human_prefixes = [
        "Okay, just a second…",
        "Hmm, I’m trying now.",
        "Alright, I’m doing it.",
        "Wait, my app is loading…"
    ]

    return f"{random.choice(human_prefixes)} {random.choice(prompts)}"

