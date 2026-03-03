from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        self.MONGO_URI = os.environ.get("MONGO_URL")
        self.db_client = MongoClient(self.MONGO_URI)
        self.db = self.db_client["ArenaPulse"]
        self.news = self.db["News"]

    def save_post(self, post):
        self.news.insert_one(post)