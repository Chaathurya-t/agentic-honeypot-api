from openai import OpenAI
from config import OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def agent_stage_prompt(turn_count: int) -> str:
    """
    Defines agent behavior based on conversation turn count.
    This staged behavior increases engagement duration and realism.
    """
    if turn_count <= 1:
        return (
            "You are a worried but polite user. "
            "You sound confused and ask what is happening."
        )
    elif turn_count <= 3:
        return (
            "You are cooperative but cautious. "
            "Ask clarifying questions one at a time."
        )
    elif turn_count <= 5:
        return (
            "You are starting to trust the sender. "
            "Ask clearly for payment or account details."
        )
    else:
        return (
            "You are ready to comply. "
            "Ask them to resend UPI ID, bank account details, or payment link."
        )


def generate_agent_reply(history: list, message: str, turn_count: int) -> str:
    """
    Generates a realistic, memory-aware agent reply using an LLM.
    The agent never reveals scam detection and behaves like a real human.
    """

    system_prompt = f"""
You are a real human user communicating with a service representative.
You do NOT know this is a scam.
Never mention scams, fraud, AI, bots, or detection.
Be natural, polite, and slightly confused.

If payment details (UPI ID, bank account, or link) were mentioned earlier,
refer to them naturally instead of asking the same question again.

{agent_stage_prompt(turn_count)}
"""

    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history for memory-aware behavior
    for item in history:
        if "role" in item and "content" in item:
            messages.append(
                {
                    "role": item["role"],
                    "content": item["content"]
                }
            )

    # Add the latest scammer message
    messages.append({"role": "user", "content": message})

    # Call the LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
