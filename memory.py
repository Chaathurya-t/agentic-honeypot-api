import time

conversation_store = {}

def get_state(conversation_id):
    if conversation_id not in conversation_store:
        conversation_store[conversation_id] = {
            "start_time": time.time(),
            "turns": 0,
            "scam_score": 0,
            "agent_active": False,
            "intelligence": {
                "bank_accounts": [],
                "upi_ids": [],
                "phishing_links": [],
                "phone_numbers": []
            }
        }
    return conversation_store[conversation_id]
