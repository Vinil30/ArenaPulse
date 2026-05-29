# ArenaPulse

ArenaPulse is an autonomous AI news platform that searches the web, turns fresh source material into structured news articles, generates matching visuals, stores the results in MongoDB, and presents them through a polished Flask web experience with an AI chat assistant.

It is designed as both a product prototype and an engineering portfolio project: easy for non-technical reviewers to understand, but deep enough to show agent orchestration, LLM integration, data persistence, frontend polish, and production-minded failure handling.

## Why It Matters

Modern news discovery is noisy. ArenaPulse compresses the workflow of finding, reading, summarizing, illustrating, and publishing a story into a single agent-driven pipeline.

For a recruiter or hiring manager, this project demonstrates:

- Product thinking: turns a broad problem, information overload, into a usable editorial experience.
- Full-stack execution: Flask backend, Jinja frontend, MongoDB persistence, and API-backed AI services.
- Agentic AI design: LangGraph coordinates search, generation, image creation, and saving.
- Practical reliability: invalid AI outputs are detected before saving, and the pipeline retries automatically.
- User experience focus: responsive UI, lazy-loaded media, SEO metadata, and loading states for async actions.

## Product Pitch

ArenaPulse acts like a lightweight AI newsroom. A user clicks "Run Agent", and the system:

1. Searches for a current trending topic.
2. Extracts source content from the web.
3. Generates a concise, factual article.
4. Creates an image prompt and matching AI image.
5. Saves the finished story.
6. Displays it in a browsable news interface.
7. Lets users ask follow-up questions through a chat assistant.

The result is a fast, visual, source-backed news feed powered by autonomous AI workflows.

## Core Features

- Autonomous news pipeline using LangGraph
- Tavily-powered web search and source extraction
- LLM-based article generation with structured JSON output
- Topic classification across sports, tech, space, health, finance, entertainment, and more
- Hugging Face image generation for article visuals
- MongoDB storage for generated posts
- Flask routes for news, chat, and agent execution
- Interactive AI chat assistant
- SEO-friendly homepage metadata and structured data
- Lazy-loaded article images with first-image priority loading
- Loading states on async buttons
- Retry protection when the generated article is an error response

## Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Backend | Flask | Web server, routing, API endpoints |
| Agent Orchestration | LangGraph | Multi-step AI pipeline |
| Search | Tavily | Current web content discovery |
| LLM API | Groq-compatible OpenAI client | News article generation and chat |
| Image Generation | Hugging Face Inference | Article image creation |
| Database | MongoDB | Persistent article storage |
| Frontend | HTML, CSS, Jinja, JavaScript | Responsive news and chat UI |
| Environment | python-dotenv | Local configuration |

## Architecture

The main agent workflow lives in `utils/Graph.py`.

```text
WebScrapper -> PostGenerator -> ImageGenerator -> SaveToDB
```

### Pipeline Steps

1. `WebScrapper`
   Picks a topic and fetches a current source using Tavily.

2. `PostGenerator`
   Sends source content to the LLM and expects a structured article object:

   ```json
   {
     "title": "Article title",
     "content": "Short news article",
     "image_prompt": "Prompt for image generation",
     "source_url": "https://source.example",
     "topic": "tech"
   }
   ```

3. `ImageGenerator`
   Generates a JPEG image from the article's image prompt and stores it as base64.

4. `SaveToDB`
   Persists valid generated articles in MongoDB.

5. Retry Guard
   If the generated result is an error article, for example:

   ```json
   {
     "title": "Error",
     "content": "The provided summary does not contain sufficient information to generate a coherent news article."
   }
   ```

   the app does not save it as a successful article. The `/run-agent` route retries the pipeline up to three times.

## Project Structure

```text
ArenaPulse/
|-- app.py                  # Flask app and route definitions
|-- requirements.txt        # Python dependencies
|-- templates/
|   |-- index.html          # News feed UI
|   |-- chat.html           # AI chat assistant UI
|   `-- about.html          # Product/about page
|-- static/
|   |-- style.css           # Shared/static styling
|   `-- script.js           # Shared/static JavaScript helpers
`-- utils/
    |-- Graph.py            # LangGraph agent workflow
    |-- arena_pulse.py      # LLM article generation
    |-- image_generator.py  # Hugging Face image generation
    |-- web_scrapper.py     # Tavily search integration
    |-- chatbot.py          # Chat assistant logic
    `-- database.py         # MongoDB integration
```

## Routes

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/` | Displays the latest generated articles |
| `POST` | `/run-agent` | Runs the full AI news pipeline |
| `GET` | `/chat` | Opens the chat assistant interface |
| `POST` | `/chat-api` | Sends a user message to the assistant |
| `GET` | `/about` | Shows the project/product overview page |

## Local Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ArenaPulse
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
groq_api_key=your_groq_key
GROQ_URI=https://api.groq.com/openai/v1
HF_API_KEY=your_huggingface_token
search_api_key=your_tavily_key
MONGO_URL=your_mongodb_connection_string
FLASK_DEBUG=False
PORT=5000
```

### 5. Run the App

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `groq_api_key` | Yes | API key for the LLM provider |
| `GROQ_URI` | Yes | Groq-compatible OpenAI API base URL |
| `HF_API_KEY` | Yes | Hugging Face token for image generation |
| `search_api_key` | Yes | Tavily search API key |
| `MONGO_URL` | Yes | MongoDB connection string |
| `PORT` | No | Flask port, defaults to `5000` |
| `FLASK_DEBUG` | No | Enables Flask debug mode when set to `True` |

## SEO and UX Work

The homepage includes:

- Descriptive title and meta description
- Canonical URL
- Open Graph and Twitter card metadata
- JSON-LD structured data
- Native image lazy loading for below-the-fold cards
- High-priority eager loading for the first article image
- Async image decoding
- Loading shimmer while images resolve
- Button-level loading states for agent and chat actions

These details make the project stronger both as a user-facing prototype and as a portfolio artifact.

## Reliability and Safety

ArenaPulse includes safeguards for generated content:

- The system prompt asks for factual, safe, non-explicit, non-defamatory summaries.
- The generated article must follow a structured JSON format.
- Error-like article outputs are filtered before image generation and saving.
- The agent route retries if the pipeline produces only invalid articles.
- Source URLs are preserved so users can verify the original material.

## Deployment Notes

ArenaPulse can be deployed as a standard Flask web service.

For Render or a similar platform:

```text
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

Add all required environment variables in the hosting dashboard.

Because image generation runs through Hugging Face Inference, the app does not require a GPU on the hosting server.

## Portfolio Talking Points

Use this project to discuss:

- How agentic workflows differ from single LLM calls
- Why structured outputs matter for AI applications
- How to add retry logic around uncertain model behavior
- How UX details like loading states improve trust in long-running AI tasks
- How SEO and performance considerations apply even to AI-generated content
- How full-stack systems connect APIs, databases, frontend rendering, and user interaction

## Future Improvements

- Scheduled background runs using cron or a task queue
- Pagination or infinite scroll for larger article sets
- Authentication and saved user preferences
- Admin review workflow before publishing generated posts
- Better duplicate detection across sources
- Redis caching for faster homepage loads
- Background workers with Celery or RQ
- Streaming progress updates during agent execution
- Automated tests for pipeline validation and route behavior

## Summary

ArenaPulse is a full-stack AI product prototype that shows how autonomous agents can transform web information into a polished, searchable, and visual news experience. It combines technical depth with a clear product story, making it suitable for demos, recruiter reviews, portfolio walkthroughs, and continued experimentation.
