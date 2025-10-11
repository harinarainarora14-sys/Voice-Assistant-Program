from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from fuzzywuzzy import fuzz
import requests
import string
import logging
from typing import Optional

# ------------------------
# Setup logging
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ------------------------
# Gemini AI Configuration
# ------------------------
GEMINI_API_KEY = "AIzaSyB4oYXN34edV8imQd7A_pYxuSSm9Hl5sso"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

# ------------------------
# Load responses
# ------------------------
try:
    with open("responses.json", "r") as f:
        responses = json.load(f)
    logger.info("✅ Successfully loaded responses.json")
except Exception as e:
    logger.error(f"⚠️ Error loading responses.json: {e}")
    responses = {}

# ------------------------
# Initialize FastAPI
# ------------------------
app = FastAPI(
    title="Enhanced Voice Assistant API",
    description="AI-powered voice assistant with Gemini integration and predefined responses",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Health check endpoint
# ------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
        "version": "2.0.0",
        "features": ["gemini_ai", "predefined_responses", "voice_support", "chat_mode"]
    }

# ------------------------
# Home & ping routes
# ------------------------
@app.get("/")
def home():
    return {
        "message": "✅ Enhanced Voice Assistant API is running",
        "version": "2.0.0",
        "endpoints": {
            "/ask": "Main chat endpoint",
            "/health": "Health check",
            "/ping": "Simple ping test"
        }
    }

@app.get("/ping")
def ping():
    return {"message": "pong", "timestamp": datetime.now().isoformat()}

# ------------------------
# Gemini AI Integration
# ------------------------
def query_gemini_ai(question: str) -> Optional[str]:
    """Query Gemini AI for general responses"""
    try:
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"You are Aina, a helpful voice assistant. Answer this question naturally and conversationally: {question}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 200,
            }
        }
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                logger.info(f"✅ Gemini AI response received for: {question[:50]}...")
                return content.strip()
        else:
            logger.error(f"❌ Gemini API error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error querying Gemini AI: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error querying Gemini AI: {e}")
    
    return None

# ------------------------
# Main ask endpoint
# ------------------------
@app.get("/ask")
def ask(question: str = Query(..., min_length=1, max_length=500)):
    """
    Main endpoint for asking questions to the voice assistant.
    Supports both predefined responses and AI-generated responses via Gemini.
    """
    try:
        # Log the incoming question
        logger.info(f"📝 Question received: {question}")
        
        # Clean the question
        original_question = question
        question = question.lower().strip()
        question = question.rstrip(string.punctuation + "!?")

        # --- Step 1: Check for exact matches in predefined responses ---
        for intent, data in responses.items():
            for q in data.get("question", []):
                if question == q.lower().strip():
                    logger.info(f"✅ Exact match found: {intent}")
                    return process_predefined_answer(intent, original_question)

        # --- Step 2: Fuzzy match for predefined responses ---
        best_match = None
        best_score = 0
        for intent, data in responses.items():
            for q in data.get("question", []):
                score = fuzz.ratio(question, q.lower())
                if score > best_score:
                    best_score = score
                    best_match = intent

        if best_match and best_score >= 85:
            logger.info(f"✅ Fuzzy match found: {best_match} (score: {best_score})")
            return process_predefined_answer(best_match, original_question)

        # --- Step 3: Use Gemini AI for general questions ---
        logger.info("🤖 Using Gemini AI for response")
        ai_response = query_gemini_ai(original_question)
        
        if ai_response:
            return {
                "answer": ai_response,
                "type": "ai_generated",
                "source": "gemini"
            }

        # --- Step 4: Fallback response ---
        logger.warning(f"⚠️ No response available for: {original_question}")
        return {
            "answer": "I'm sorry, I'm having trouble understanding that right now. Could you try asking in a different way?",
            "type": "fallback"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in ask endpoint: {e}")
        return {
            "answer": "I'm experiencing some technical difficulties. Please try again in a moment.",
            "type": "error"
        }

# ------------------------
# Answer processing for predefined responses
# ------------------------
def process_predefined_answer(intent: str, question: str):
    """Process predefined answers with special handling for time and other dynamic content"""
    try:
        answer = responses[intent].get("answer", "Sorry, I don't understand that.")

        # Time request → Indian local time 12-hour format
        if answer.upper() == "TIME":
            india_tz = ZoneInfo("Asia/Kolkata")
            now_india = datetime.now(india_tz)
            time_str = now_india.strftime("%I:%M %p")
            date_str = now_india.strftime("%A, %B %d, %Y")
            return {
                "answer": f"The current time in India is {time_str} on {date_str}",
                "type": "time_india",
                "source": "predefined"
            }

        # Regular predefined response
        return {
            "answer": answer,
            "type": "predefined",
            "intent": intent,
            "source": "predefined"
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing predefined answer: {e}")
        return {
            "answer": "I encountered an issue processing that request.",
            "type": "error",
            "source": "system"
        }

# ------------------------
# Debug endpoint for troubleshooting
# ------------------------
@app.get("/debug-gemini")
def debug_gemini():
    """Debug endpoint to test Gemini AI integration"""
    try:
        # Test the Gemini API
        test_question = "What is 2+2?"
        test_response = query_gemini_ai(test_question)
        
        return {
            "status": "debug_info",
            "api_key_configured": bool(GEMINI_API_KEY),
            "api_key_length": len(GEMINI_API_KEY) if GEMINI_API_KEY else 0,
            "api_url": GEMINI_API_URL,
            "test_question": test_question,
            "test_response": test_response,
            "responses_loaded": len(responses),
            "sample_intents": list(responses.keys())[:5] if responses else [],
            "fallback_message": "I'm sorry, I'm having trouble understanding that right now. Could you try asking in a different way?"
        }
    except Exception as e:
        return {
            "status": "debug_error",
            "error": str(e),
            "api_key_configured": bool(GEMINI_API_KEY)
        }

# ------------------------
# Additional utility endpoints
# ------------------------
@app.get("/intents")
def get_available_intents():
    """Get list of available predefined intents"""
    return {
        "intents": list(responses.keys()),
        "count": len(responses),
        "description": "Available predefined responses that can be customized for different projects"
    }

@app.get("/intent/{intent_name}")
def get_intent_details(intent_name: str):
    """Get details of a specific intent"""
    if intent_name in responses:
        return {
            "intent": intent_name,
            "questions": responses[intent_name].get("question", []),
            "answer": responses[intent_name].get("answer", ""),
            "customizable": True
        }
    else:
        raise HTTPException(status_code=404, detail="Intent not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
