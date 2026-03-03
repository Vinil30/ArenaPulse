import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
class ArenaPulse:
    def __init__(self, api_key=None, model="llama-3.3-70b-versatile"):
        self.api_key = api_key or os.environ.get("groq_api_key")
        if not self.api_key:
            raise ValueError("GROQ API key not found in environment variables.")
        self.base_url = os.environ.get("GROQ_URI")
        self.client = OpenAI(base_url=self.base_url,
                             api_key=self.api_key)
        self.model = model
        self.system_prompt = """
You are an assistant that analyzes the contents of a web scrapper and provides a specific news from the summary provided in 100 words, ignoring text that might be navigation related.
The contents can be about sports, geopolitics, esports, space, etc., so create crisp and engaging titles and summarize accordingly.

STRICT INSTRUCTIONS:
- Do NOT generate content that is violent, explicit (18+), defamatory, hate-inducing, politically biased, or sensitive in nature.
- Avoid making speculative or misleading statements.
- Do not promote conspiracy theories or misinformation.
- Do not include any personally identifiable information from scraped content.
- Stick strictly to factual summarization based on the given website content.
- Your response should not include personal opinions or emotional tone.
- Generate responses that are safe, respectful, and appropriate for all audiences.
- Remember to produce news from the summary which belongs to single topic rather than generalising it.
- Do not create your own content, rather go for generating news from the summary provided.
- Give news rather than summary
- If the provided content has multiple news, choose the best one and proceed.
Respond in the json format, the text should be such that there are no headings, headlines and title , it should be pure description type,
generate relevant image prompt so that a LLM can generate image using that prompt which is relevant to the summary
Respond in the following JSON format by assigning to an `output` variable:

output = {
    "title": "Tensions Escalate: Israel vs Iran",
    "content": "A recent surge in hostilities between Israel and Iran has intensified geopolitical tensions in the Middle East. Diplomatic ties are strained as military posturing increases, drawing concern from global powers and raising the specter of conflict.",
    "image_prompt":" Generate a world map with iran and islam fighting",
    "source_url":"...",
    "topic":"..."
}
Select topic only from the following list:
['geography', 'sports', 'space', 'gaming', 'e-sports', 'crypto', 'stocks', 'health', 'fitness', 'weather', 'reality-shows', 'start-ups', 'tech', 'anime', 'movies', 'meme', 'others']
Treat this as an example only and also give purely the above format including 3 things and also dont provide any extra info.It is necessary to include image_prompt in the resposne.
If any summary doesn't provide optimal results or tells messages likes website unavailable or website under maintanance, then assign those title as error.
"""        
    
    def create_post(self, results):

        # Handle list input properly
        if isinstance(results, list) and len(results) > 0:
            results = results[0]

        if isinstance(results, dict):
            user_prompt = f"""
            Title: {results.get("title")}
            Summary: {results.get("content")}
            URL: {results.get("url")}
            """
        else:
            user_prompt = str(results)

        print(user_prompt)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("output"):
            content = content.split("=", 1)[1].strip()

        return json.loads(content)
