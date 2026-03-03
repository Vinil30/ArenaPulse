from langgraph.graph import StateGraph, START, END
from typing import Dict, TypedDict, List
from utils.arena_pulse import ArenaPulse
from utils.image_generator import ImageforArenaPulse
from utils.web_scrapper import WebScrapper
from utils.database import Database
import base64
from io import BytesIO
class AgentState(TypedDict):
    results:List[Dict]
    posts:List[Dict]

def web_scrapping(state:AgentState)->AgentState:
    scrapper = WebScrapper()
    state["results"] = scrapper.search_agent()
    return state

def post_generation(state:AgentState)->AgentState:
    post_generator = ArenaPulse()
    for result in state["results"]:
        response = post_generator.create_post(results=result)
        state["posts"].append(response)
    return state
    

def image_generation(state: AgentState) -> AgentState:
    image_generator = ImageforArenaPulse()
    for post in state["posts"]:
        pil_image = image_generator.generate_image_arena(post["image_prompt"])
        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        post["image"] = image_base64

    return state

def save_to_db(state:AgentState)->AgentState:
    db = Database()
    for post in state["posts"]:
        db.save_post(post=post)
    return state

graph = StateGraph(AgentState)
graph.add_node("WebScrapper",web_scrapping)
graph.add_node("PostGenerator",post_generation)
graph.add_node("ImageGenerator",image_generation)
graph.add_node("SaveToDB",save_to_db)

graph.add_edge(START, "WebScrapper")
graph.add_edge("WebScrapper","PostGenerator")
graph.add_edge("PostGenerator", "ImageGenerator")
graph.add_edge("ImageGenerator", "SaveToDB")
graph.add_edge("SaveToDB", END)

