import os
from dotenv import load_dotenv
from tavily import TavilyClient
import random
class WebScrapper:
    def __init__(self):
        self.search_api_key = os.environ.get("search_api_key")
        self.client = TavilyClient(api_key=self.search_api_key)
        self.topics = ['geography', 'sports', 'space', 'gaming', 'e-sports', 'crypto', 'stocks', 'health', 'fitness', 'weather', 'reality-shows', 'start-ups', 'tech', 'anime', 'movies', 'meme', 'others']


    def topic_pick(self):
        topic = random.choice(self.topics)
        if topic == "others":
            search_query = "Latest Trending news in India"
        else:
            search_query = f"Latest trending news about {topic}"
        return search_query
        
    def search_agent(self):
        query = self.topic_pick()
        response = self.client.search(
            query=query,
            max_results=1,
            search_depth="advanced",
            include_raw_content=True,  
            include_answer=True,       
            include_images=False,
            include_domains=[],        
            exclude_domains=["youtube.com", "pinterest.com"]  
        )
        
        
        output = []
        for result in response["results"]:
            output.append({
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "raw_content": result.get("raw_content", ""),  
                "url": result.get("url", "")
            })
        
        return output