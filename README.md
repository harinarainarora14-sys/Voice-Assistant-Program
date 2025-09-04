🤖 Aina - Enhanced AI Voice Assistant
A powerful, customizable voice assistant API powered by Google's Gemini AI with predefined responses for specific use cases. Perfect for integration into any project!

✨ Features
🎯 Dual Intelligence System
Gemini AI Integration: Handles general conversations and complex queries
Predefined Responses: Quick, customized responses for specific topics
Smart Fallback: Seamlessly switches between AI and predefined responses
🎙️ Multi-Modal Interface
Chat Mode: Text input with integrated mic button for mixed interaction
Voice Chat: Single voice interaction mode
Continuous Voice: Hands-free conversation mode
Real-time Processing: Instant responses with typing indicators
🛠️ Developer-Friendly
RESTful API: Easy integration with any frontend
Customizable Knowledge Base: Modify responses.json for different projects
CORS Enabled: Works with any web application
Health Monitoring: Built-in health check endpoints
🎨 Modern UI
Beautiful Design: Gradient backgrounds and smooth animations
Mobile Responsive: Works perfectly on all devices
Dark Theme: Easy on the eyes
Chat Interface: Familiar messaging app experience
🚀 Quick Start
Backend Setup
Install Dependencies
bash
pip install -r requirements.txt
Run the Server
bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
Test the API
bash
curl "http://localhost:8000/ask?question=Hello"
Frontend Setup
Simply open index.html in a web browser or serve it through any web server.

📡 API Endpoints
Main Endpoints
GET / - API information and status
GET /ask?question=<your_question> - Main chat endpoint
GET /health - Health check with system info
GET /ping - Simple connectivity test
Utility Endpoints
GET /intents - List all available predefined responses
GET /intent/<intent_name> - Get details of specific intent
Example API Usage
javascript
// Basic request
const response = await fetch('http://your-api-url/ask?question=Hello');
const data = await response.json();
console.log(data.answer); // "Hello! I'm Aina, your AI voice assistant..."

// Response includes metadata
console.log(data.type);    // "predefined" or "ai_generated"
console.log(data.source);  // "gemini" or "predefined"
🔧 Customization
Modifying Predefined Responses
Edit responses.json to customize the assistant for your specific project:

json
{
  "your_custom_intent": {
    "question": ["how to use your app", "app help", "guide"],
    "answer": "Here's how to use our amazing app..."
  }
}
Changing API Base URL
Update the API base URL in the frontend:

javascript
// In index.html, modify this line:
let apiBase = "https://your-deployed-api-url.com";
Gemini AI Configuration
Replace the API key in app.py:

python
GEMINI_API_KEY = "your_gemini_api_key_here"
🌟 Use Cases
💼 Business Applications
Customer support chatbots
Product information assistants
FAQ automation
Lead generation tools
🏫 Educational Projects
Interactive learning assistants
Quiz and Q&A systems
Language learning companions
Study helpers
🏥 Healthcare & Wellness
Mental health support bots
Medication reminders
Wellness coaching
Symptom checkers
🏠 Personal Projects
Smart home assistants
Personal productivity tools
Entertainment companions
Daily routine helpers
📦 Project Structure
voice-assistant-api/
├── app.py              # FastAPI backend with Gemini integration
├── responses.json      # Customizable knowledge base
├── requirements.txt    # Python dependencies
├── index.html         # Frontend interface
├── .gitignore         # Git ignore rules
└── README.md          # This file
🔒 Security Features
Input Validation: Prevents malicious inputs
Rate Limiting Ready: Easily add rate limiting
CORS Protection: Configurable CORS policies
Error Handling: Graceful error responses
Logging: Built-in request logging
🚀 Deployment Options
Option 1: Render.com (Recommended)
Connect your GitHub repository
Set build command: pip install -r requirements.txt
Set start command: uvicorn app:app --host 0.0.0.0 --port $PORT
Option 2: Railway
Connect repository
Railway auto-detects Python and FastAPI
Deploys automatically
Option 3: Heroku
Create Procfile: web: uvicorn app:app --host 0.0.0.0 --port $PORT
Push to Heroku
Set environment variables if needed
Option 4: Docker
dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
🔮 Advanced Features Coming Soon
Multi-language Support: Conversation in multiple languages
Voice Cloning: Custom voice personalities
Context Memory: Remember conversation history
Plugin System: Extend with custom modules
Analytics Dashboard: Usage statistics and insights
WebSocket Support: Real-time bidirectional communication
🤝 Integration Examples
React Integration
jsx
const askAssistant = async (question) => {
  const response = await fetch(`${API_BASE}/ask?question=${encodeURIComponent(question)}`);
  return await response.json();
};
Vue.js Integration
vue
<script>
export default {
  methods: {
    async sendMessage(question) {
      const response = await fetch(`${this.apiBase}/ask?question=${encodeURIComponent(question)}`);
      return await response.json();
    }
  }
}
</script>
Mobile App Integration
javascript
// React Native / Expo
const sendToAssistant = async (message) => {
  try {
    const response = await fetch(`${API_URL}/ask?question=${encodeURIComponent(message)}`);
    const data = await response.json();
    return data.answer;
  } catch (error) {
    console.error('Assistant error:', error);
  }
};
📈 Performance Tips
Cache Responses: Implement Redis caching for frequently asked questions
Load Balancing: Use multiple instances for high traffic
CDN Integration: Serve static frontend files through CDN
Database Integration: Store user preferences and conversation history
Monitoring: Use tools like Sentry for error tracking
🛟 Troubleshooting
Common Issues
Voice Recognition Not Working

Ensure HTTPS connection (required for microphone access)
Check browser permissions
Test with different browsers
API Connection Issues

Verify API URL is correct
Check CORS configuration
Ensure backend is running
Gemini API Errors

Verify API key is valid
Check API quotas and limits
Review request format
📄 License
This project is open source and available under the MIT License.

🤖 About Aina
Aina (meaning "mirror" or "reflection" in some languages) is designed to reflect your needs and adapt to different projects while maintaining powerful AI capabilities. Whether you need a customer service bot, educational assistant, or personal companion, Aina can be customized to fit your requirements.

Made with ❤️ for developers who want to build amazing voice-enabled applications.

For questions, issues, or contributions, please visit our GitHub repository.

