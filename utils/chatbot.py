import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

load_dotenv()

class ChatBot:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ["groq_api_key"]
        )
        self.tavily = TavilyClient(api_key=os.environ["search_api_key"])
        self.messages = [{"role": "system", "content": "You are a News Assistant. For latest news, use search_news."}]

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=self.messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "search_news",
                        "description": "Search latest news from the web",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "News search query"}
                            },
                            "required": ["query"]
                        }
                    }
                }],
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            if hasattr(message, 'tool_calls') and message.tool_calls:
                tool_call = message.tool_calls[0]
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                if function_name == "search_news":
                    search_result = self.tavily.search(
                        query=arguments["query"],
                        search_depth="basic",
                        max_results=3
                    )
                    
                    formatted_results = f"Search results for '{arguments['query']}':\n\n"
                    for i, result in enumerate(search_result.get('results', []), 1):
                        formatted_results += f"{i}. {result.get('title', 'No title')}\n"
                        formatted_results += f"   {result.get('content', 'No content')}\n"
                        formatted_results += f"   URL: {result.get('url', 'No URL')}\n\n"
                    
                    self.messages.append({
                        "role": "assistant",
                        "content": "",
                        "tool_calls": message.tool_calls
                    })
                    
                    self.messages.append({
                        "role": "tool",
                        "content": formatted_results,
                        "tool_call_id": tool_call.id
                    })
                    
                    final_response = self.client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=self.messages
                    )
                    
                    result = final_response.choices[0].message.content
                    self.messages.append({"role": "assistant", "content": result})
                    
                else:
                    result = f"I tried to call {function_name} but it's not available."
            else:
                result = message.content
                self.messages.append({"role": "assistant", "content": result})
                
        except Exception as e:
            result = f"Error: {str(e)}"
            
        if len(self.messages) > 12:
            self.messages = [self.messages[0]] + self.messages[-(12 - 1):]
        
        return result