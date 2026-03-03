import os
from dotenv import load_dotenv
from tavily import TavilyClient

class WebScrapper:
    def __init__(self):
        self.search_api_key = os.environ.get("search_api_key")
        self.query = "What are the average Nitrogen, phospohorus and potassium values in agriculture land of Nirmal, Telangana, india"
        self.client = TavilyClient(api_key=self.search_api_key)
    def search_agent(self):
        response = self.client.search(
            query=self.query,
            max_results=1,
            search_depth="advanced",
            include_raw_content=False,
            include_answer=False,
            include_images = False
        )

        output = response["results"]
        return output