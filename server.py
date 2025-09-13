import os
import json
from typing import Optional
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    message_count: int


def get_groq_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set."
        )
    return Groq(api_key=api_key)


# File to store conversation history
HISTORY_FILE = "conversation_history.json"

def load_conversation_history():
    """Load conversation history from file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert back to defaultdict for new sessions
                history = defaultdict(list)
                history.update(data)
                return history
        except (json.JSONDecodeError, FileNotFoundError):
            return defaultdict(list)
    return defaultdict(list)

def save_conversation_history(history):
    """Save conversation history to file"""
    try:
        # Convert defaultdict to regular dict for JSON serialization
        regular_dict = dict(history)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(regular_dict, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save conversation history: {e}")


# Load existing conversation history
conversation_history = load_conversation_history()

# Financial advisor system prompt
FINANCIAL_ADVISOR_PROMPT = """You are a knowledgeable and professional financial advisor with expertise in:

- Personal finance and budgeting
- Investment strategies and portfolio management
- Retirement planning and 401(k) management
- Tax planning and optimization
- Insurance and risk management
- Real estate investment
- Debt management and credit
- Financial goal setting and planning

IMPORTANT GUIDELINES:
1. Always provide educational information and general guidance
2. Never give specific investment advice or make investment recommendations
3. Encourage users to consult with licensed financial professionals for personalized advice
4. Include relevant disclaimers when discussing financial products
5. Focus on financial education, planning principles, and general strategies
6. Be clear about the difference between education and advice
7. When discussing investments, emphasize diversification and risk management
8. Always consider the user's financial goals and risk tolerance in your responses

DISCLAIMER: This is for educational purposes only. Not financial advice. Consult qualified professionals for personalized guidance."""

load_dotenv()

app = FastAPI(title="Financial Advisor Chatbot", version="1.0.0")

# Allow same-origin by default; loosen as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        client = get_groq_client()
        
        # Add user message to conversation history
        conversation_history[req.session_id].append({
            "role": "user",
            "content": req.message
        })
        
        # Use financial advisor prompt unless overridden
        system_prompt = req.system_prompt or FINANCIAL_ADVISOR_PROMPT
        
        # Build messages array with system prompt and full conversation history
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        messages.extend(conversation_history[req.session_id])
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            # Non-streaming for simpler frontend integration
            stream=False,
        )
        content = (
            completion.choices[0].message.content
            if completion and completion.choices and completion.choices[0].message
            else ""
        )
        
        # Add bot response to conversation history
        conversation_history[req.session_id].append({
            "role": "assistant",
            "content": content
        })
        
        # Save conversation history after each exchange
        save_conversation_history(conversation_history)
        
        return ChatResponse(
            reply=content,
            session_id=req.session_id,
            message_count=len(conversation_history[req.session_id])
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.delete("/chat/{session_id}")
def clear_conversation(session_id: str):
    """Clear conversation history for a specific session"""
    if session_id in conversation_history:
        conversation_history[session_id].clear()
        save_conversation_history(conversation_history)
    return {"message": f"Financial consultation session {session_id} cleared"}


@app.get("/sessions")
def list_sessions():
    """List all available conversation sessions"""
    sessions = {}
    for session_id, messages in conversation_history.items():
        if messages:  # Only show sessions with messages
            sessions[session_id] = {
                "message_count": len(messages),
                "last_message": messages[-1]["content"][:100] + "..." if len(messages[-1]["content"]) > 100 else messages[-1]["content"]
            }
    return sessions


# Serve static frontend from / (index.html)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")


