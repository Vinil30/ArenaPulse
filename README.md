# 📰 ArenaPulse — AI Autonomous News Engine

ArenaPulse is an agentic AI-powered news generation platform that autonomously scrapes web data, generates factual news articles using LLMs, creates AI-generated images, stores structured content in MongoDB, and provides an interactive AI news assistant. It is built using Flask, LangGraph, HuggingFace Inference, Groq LLMs, Tavily Search, and MongoDB.

------------------------------------------------------------

🏗️ PROJECT STRUCTURE

ArenaPulse/
│
├── app.py                     # Flask application (main entry)
├── .env                       # Environment variables
│
├── templates/                 # Frontend (Jinja Templates)
│   ├── base.html
│   ├── index.html
│   ├── chat.html
│   └── about.html
│
├── utils/
│   ├── Graph.py               # LangGraph pipeline definition
│   ├── arena_pulse.py         # LLM news generation module
│   ├── image_generator.py     # AI image generation (HF Inference)
│   ├── web_scrapper.py        # Tavily search agent
│   ├── chatbot.py             # AI chat assistant
│   └── database.py            # MongoDB integration
│
├── requirements.txt
└── README.md

------------------------------------------------------------

⚙️ ARCHITECTURE

LangGraph Pipeline Flow:

WebScrapper → PostGenerator → ImageGenerator → SaveToDB

1. WebScrapper fetches relevant content via Tavily.
2. ArenaPulse LLM module generates structured news JSON.
3. ImageGenerator creates AI-generated images via HF Inference.
4. News is stored in MongoDB.
5. Frontend dynamically renders the content.
6. Chatbot provides real-time AI-powered news assistance.

------------------------------------------------------------

🚀 LOCAL SETUP

1) Clone Repository
git clone <your_repo_url>
cd ArenaPulse

2) Create Virtual Environment
python -m venv venv
source venv/bin/activate     (Mac/Linux)
venv\Scripts\activate        (Windows)

3) Install Dependencies
pip install -r requirements.txt

4) Configure Environment Variables (.env)

groq_api_key=your_groq_key
GROQ_URI=https://api.groq.com/openai/v1
HF_API_KEY=your_huggingface_token
search_api_key=your_tavily_key
MONGO_URL=your_mongodb_connection_string

5) Run Application
python app.py

App runs at:
http://127.0.0.1:5000

------------------------------------------------------------

🌐 DEPLOYMENT (RENDER)

1. Push project to GitHub.
2. Create a new Web Service on Render.
3. Build Command:
   pip install -r requirements.txt
4. Start Command:
   python app.py
5. Add environment variables in Render dashboard.

Since image inference runs remotely via HuggingFace, no GPU is required for deployment.

------------------------------------------------------------

🔌 ROUTES

GET    /            → View latest news
POST   /run-agent   → Run full AI news pipeline
GET    /chat        → Chat interface
POST   /chat-api    → Chatbot API
GET    /about       → About page

------------------------------------------------------------

🧠 AI STACK

- Groq (LLM inference)
- HuggingFace Inference (Image generation)
- Tavily (Search)
- LangGraph (Agent orchestration)
- MongoDB (Data storage)
- Flask (Backend framework)

------------------------------------------------------------

📦 FEATURES

AI Pipeline:
- Autonomous news extraction
- Structured JSON output
- Topic classification
- Image prompt generation
- Base64 image storage

Frontend:
- Modern glassmorphism UI
- Responsive layout
- Interactive hover animations
- Loading indicators
- AI chat assistant

Backend:
- Agent-based workflow
- Retry handling
- Modular architecture
- Clean separation of concerns

------------------------------------------------------------

🛡️ SAFETY CONTROLS

- No harmful or explicit content
- No political bias
- No misinformation
- Strict factual summarization
- Structured JSON-only output

------------------------------------------------------------

🎯 USE CASES

- AI automation demos
- Agentic system showcase
- Hackathon project
- Portfolio project
- Research prototype

------------------------------------------------------------

🚀 FUTURE IMPROVEMENTS

- Scheduled auto execution (cron jobs)
- Pagination and infinite scroll
- User authentication
- Background task queue (Celery)
- Redis caching
- Microservice separation
- Real-time streaming updates

------------------------------------------------------------

ArenaPulse — Intelligent, Autonomous News Generation System.