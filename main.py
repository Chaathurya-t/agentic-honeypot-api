from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import time

from config import API_KEY
from memory import get_state
from detector import update_scam_score
from extractor import extract_intelligence
from agent import generate_agent_reply
from fallback import fallback_reply

app = FastAPI(
    title="Agentic Honeypot API",
    description="Scam Detection & Intelligence Extraction System",
    version="1.0.0"
)

# -------------------------------------------------
# ROOT ENDPOINT (GET)
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
# ROOT ENDPOINT (POST) ⭐ REQUIRED FOR TESTER ⭐
# -------------------------------------------------
@app.post("/")
async def root_post(request: Request, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Accept ANY JSON body without validation
    return {
        "status": "ok",
        "message": "Honeypot endpoint reachable"
    }

# -------------------------------------------------
# REQUEST SCHEMA
# -------------------------------------------------
class MessageInput(BaseModel):
    conversation_id: str = ""
    message: str = ""
    history: list = []

# -------------------------------------------------
# MAIN HONEYPOT ENDPOINT
# -------------------------------------------------
@app.post("/process-message")
def process_message(
    data: MessageInput,
    x_api_key: str = Header(None),
    authorization: str = Header(None)
):
    if not (x_api_key == API_KEY or authorization == f"Bearer {API_KEY}"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not data.message:
        return {"status": "ok"}

    state = get_state(data.conversation_id)
    state["turns"] += 1

    scam_score = update_scam_score(data.message, state)

    agent_reply = None
    if scam_score or state["agent_active"]:
        state["agent_active"] = True
        try:
            agent_reply = generate_agent_reply(
                data.history,
                data.message,
                state["turns"]
            )
        except Exception:
            agent_reply = fallback_reply()

    extract_intelligence(
        data.message,
        state["intelligence"],
        state["turns"]
    )

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
