import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient
import random

load_dotenv()

class ChatBot:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ["groq_api_key"]
        )
        self.tavily = TavilyClient(api_key=os.environ["search_api_key"])
        
        # Available topics for random news
        self.topics = ['geography', 'sports', 'space', 'gaming', 'e-sports', 'crypto', 
                       'stocks', 'health', 'fitness', 'weather', 'reality-shows', 
                       'start-ups', 'tech', 'anime', 'movies', 'meme', 'others']
        
        self.messages = [{
            "role": "system", 
            "content": """You are a News Assistant. Help users find latest news and information.

**IMPORTANT FORMATTING RULES:**
- Always respond using clean markdown only
- Use **bold** for important information
- Use bullet points with - for lists
- Use ### for section headers
- Use > for quotes or important callouts
- Never include HTML tags, divs, or complex formatting
- Keep markdown clean and simple
- Use [text](url) for links
- Keep responses well-structured but minimal in markdown syntax

**YOUR CAPABILITIES:**
- You can search for current news and information
- When users ask about news, latest events, or current information, you should respond with up-to-date information
- You have access to real-time news data

When presenting news:
1. Start with a brief summary
2. Use bullet points with - for key stories
3. Include source attribution
4. Be concise but informative"""
        }]

    def search_news(self, query: str) -> str:
        """Search for news using Tavily and format results in clean markdown"""
        try:
            search_query = query
            
            if "random" in query.lower() or not query.strip():
                topic = random.choice(self.topics)
                if topic == "others":
                    search_query = "Latest Trending news"
                else:
                    search_query = f"Latest trending news about {topic}"
            
            response = self.tavily.search(
                query=search_query,
                max_results=3,
                search_depth="advanced",
                include_raw_content=True,
                include_answer=False,
                include_images=False,
                exclude_domains=["youtube.com", "instagram.com", "pinterest.com", "flickr.com", "tiktok.com"]
            )
            
            formatted_results = []
            for result in response.get('results', []):
                content = result.get('raw_content') or result.get('content', '')
                content = ' '.join(content.split())
                
                if len(content) > 800:
                    content = content[:800] + "..."
                
                formatted_results.append({
                    "title": result.get('title', 'No title'),
                    "content": content,
                    "url": result.get('url', 'No URL'),
                    "source": result.get('url', '').split('/')[2] if result.get('url') else 'Unknown'
                })
            
            if formatted_results:
                output = f"### 📰 News: {search_query}\n\n"
                for i, res in enumerate(formatted_results, 1):
                    output += f"**{i}. {res['title']}**\n\n"
                    output += f"*Source: {res['source']}*\n\n"
                    output += f"{res['content']}\n\n"
                    output += f"[Read full article]({res['url']})\n\n"
                    output += "---\n\n"
                return output
            else:
                return f"No Results No news found for '{search_query}'. Please try a different topic."
                
        except Exception as e:
            return f"Error Failed to search news: {str(e)}"

    def chat(self, user_input: str) -> str:
        """Main chat function with intelligent search"""
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            news_keywords = ['news', 'latest', 'trending', 'today', 'current', 
                            'happening', 'update', 'stories', 'headlines', 'random',
                            't20', 'world cup', 'finals', 'match', 'score', 'result']
            
            needs_search = any(keyword in user_input.lower() for keyword in news_keywords)
            
            if needs_search:
                search_query = user_input
                
                if any(term in user_input.lower() for term in ['t20', 'world cup', 'finals', 'match']):
                    search_query = f"{user_input} match result score"
                elif "summarize" in user_input.lower() or "top stories" in user_input.lower():
                    search_query = "top news stories today"
                elif "technology" in user_input.lower() or "tech" in user_input.lower():
                    search_query = "latest technology news"
                elif "world" in user_input.lower():
                    search_query = "world news headlines"
                
                search_results = self.search_news(search_query)                
                context = f"""Based on the following search results, answer the user's question.

**CRITICAL FORMATTING INSTRUCTION:**
- Respond using ONLY clean markdown
- Use **bold** for emphasis
- Use bullet points with - for lists
- Use ### for section headers
- Use > for important notes
- Use [text](url) for links
- Keep markdown simple and clean
- NO HTML tags, NO divs, NO spans, NO complex styling

**Search Results:**
{search_results}

**User's Question:** {user_input}
Provide a helpful, well-formatted markdown response."""
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": self.messages[0]["content"]},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
                
                result = response.choices[0].message.content
                
            else:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=self.messages,
                    temperature=0.7,
                    max_tokens=500
                )
                result = response.choices[0].message.content
            
            self.messages.append({"role": "assistant", "content": result})
            
            if len(self.messages) > 12:
                self.messages = [self.messages[0]] + self.messages[-(12 - 1):]
            
            return result
            
        except Exception as e:
            error_msg = f"Error\n\nI encountered an issue: {str(e)}\n\nPlease try asking your question differently."
            return error_msg