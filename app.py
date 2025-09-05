from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import string
import logging
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Gemini AI Configuration
GEMINI_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Load predefined responses
try:
    with open("responses.json", "r") as f:
        responses = json.load(f)
    logger.info("✅ Successfully loaded responses.json")
except Exception as e:
    logger.error(f"⚠️ Error loading responses.json: {e}")
    responses = {}

# Initialize FastAPI
app = FastAPI(
    title="Enhanced Voice Assistant API",
    description="AI-powered voice assistant with Gemini integration",
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

def query_gemini_ai(question: str) -> Optional[str]:
    """Query Gemini AI for responses"""
    try:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": question
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
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
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            
    except Exception as e:
        logger.error(f"❌ Gemini AI error: {e}")
    
    return None

@app.get("/ask")
def ask(question: str = Query(..., min_length=1, max_length=500)):
    """Main endpoint for asking questions"""
    try:
        # Clean the question
        question = question.strip()
        logger.info(f"📝 Question received: {question}")

        # Check for time-related queries
        if "time" in question.lower():
            india_tz = ZoneInfo("Asia/Kolkata")
            now_india = datetime.now(india_tz)
            return {
                "answer": f"The current time is {now_india.strftime('%I:%M %p')}",
                "type": "time",
                "source": "system"
            }

        # Try Gemini AI
        ai_response = query_gemini_ai(question)
        if ai_response:
            return {
                "answer": ai_response,
                "type": "ai_generated",
                "source": "gemini"
            }

        # Fallback response
        return {
            "answer": "I'm sorry, I couldn't process that request. Please try again.",
            "type": "fallback"
        }

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return {
            "answer": "I'm experiencing technical difficulties. Please try again later.",
            "type": "error"
        }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
    }

@app.get("/")
def home():
    return {"message": "Voice Assistant API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
