from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import time

from config import API_KEY
from memory import get_state
from detector import update_scam_score
from extractor import extract_intelligence
from agent import generate_agent_reply

# -------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------
app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Intelligence Extraction System",
    version="1.0.0"
)

# -------------------------------------------------
# Root Endpoint
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
    conversation_id: str
    message: str
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
    # Safety Check
    # -----------------------------
    if not data.message:
        return {"status": "ok", "message": "Honeypot service active"}

    # -----------------------------
    # Conversation State
    # -----------------------------
    state = get_state(data.conversation_id)
    state["turns"] += 1

    # -----------------------------
    # Scam Detection (score-based)
    # -----------------------------
    scam_score = update_scam_score(data.message, state)

    # 🔥 ONCE SCAM DETECTED → AGENT LOCKS IN
    if scam_score > 0:
        state["agent_active"] = True

    # -----------------------------
    # Agentic Response (NO FALLBACK)
    # -----------------------------
    agent_reply = None
    if state["agent_active"]:
        agent_reply = generate_agent_reply(
            message=data.message,
            history=data.history,
            scam_score=scam_score
        )

    # -----------------------------
    # Intelligence Extraction
    # -----------------------------
    extract_intelligence(
        data.message,
        state["intelligence"],
        state["turns"]
    )

    # -----------------------------
    # Final Structured Response
    # -----------------------------
    return {
        "scam_detected": scam_score,
        "agent_activated": state["agent_active"],
        "agent_message": agent_reply,
        "engagement_metrics": {
            "turn_count": state["turns"],
            "conversation_duration": int(time.time() - state["start_time"])
        },
        "extracted_intelligence": state["intelligence"]
    }

