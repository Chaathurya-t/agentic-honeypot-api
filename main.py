from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import time

from config import API_KEY
from memory import get_state
from detector import update_scam_score
from extractor import extract_intelligence
from agent import generate_agent_reply
from fallback import fallback_reply

# -------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------
app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Intelligence Extraction System",
    version="1.0.0"
)

# -------------------------------------------------
# Root Endpoint (UPGRADE 4 – Demo Polish)
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "Agentic Honeypot API running",
        "problem": "Scam Detection & Intelligence Extraction",
        "endpoints": {
            "process_message": "/process-message"
        }
    }

# -------------------------------------------------
# Request Schema
# -------------------------------------------------
class MessageInput(BaseModel):
    conversation_id: str = ""
    message: str = ""
    history: list = []

# -------------------------------------------------
# Main Honeypot Endpoint
# -------------------------------------------------
@app.post("/process-message")
def process_message(
    data: MessageInput,
    x_api_key: str = Header(None),
    authorization: str = Header(None)
):
    # -----------------------------
    # Authentication
    # -----------------------------
    if not (x_api_key == API_KEY or authorization == f"Bearer {API_KEY}"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # -----------------------------
    # Tester Safety (empty message)
    # -----------------------------
    if not data.message:
        return {
            "status": "ok",
            "message": "Honeypot service active"
        }

    # -----------------------------
    # Conversation State
    # -----------------------------
    state = get_state(data.conversation_id)
    state["turns"] += 1

    # -----------------------------
    # Scam Detection
    # -----------------------------
    scam_detected = update_scam_score(data.message, state)

    # -----------------------------
    # Agentic Handoff
    # -----------------------------
    agent_reply = None
    if scam_detected or state["agent_active"]:
        state["agent_active"] = True
        try:
            agent_reply = generate_agent_reply(
                data.history,
                data.message,
                state["turns"]
            )
        except Exception:
            agent_reply = fallback_reply()

    # -----------------------------
    # Progressive Intelligence Extraction (UPGRADE 3)
    # -----------------------------
    extract_intelligence(
        data.message,
        state["intelligence"],
        state["turns"]
    )

    # -----------------------------
    # Structured Response
    # -----------------------------
    return {
        "scam_detected": scam_detected,
        "agent_activated": state["agent_active"],
        "agent_message": agent_reply,
        "engagement_metrics": {
            "turn_count": state["turns"],
            "conversation_duration": int(time.time() - state["start_time"])
        },
        "extracted_intelligence": state["intelligence"]
    }
