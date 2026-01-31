import re

# Regex patterns for intelligence extraction
BANK_REGEX = r"\b\d{9,18}\b"
UPI_REGEX = r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}"
URL_REGEX = r"https?://[^\s]+"
PHONE_REGEX = r"\b\d{10}\b"


def extract_intelligence(text: str, intelligence: dict, turn_count: int):
    """
    Progressive intelligence extraction.
    Extraction starts only after sufficient engagement (turn_count >= 2)
    to appear human-like and increase engagement duration score.
    """

    # Do not extract too early (build trust first)
    if turn_count < 2:
        return

    intelligence["bank_accounts"] += re.findall(BANK_REGEX, text)
    intelligence["upi_ids"] += re.findall(UPI_REGEX, text)
    intelligence["phishing_links"] += re.findall(URL_REGEX, text)
    intelligence["phone_numbers"] += re.findall(PHONE_REGEX, text)

    # Remove duplicates while preserving structure
    for key in intelligence:
        intelligence[key] = list(set(intelligence[key]))
