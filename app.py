import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from utils.Graph import graph
from utils.database import Database
from utils.chatbot import ChatBot

load_dotenv()

app = Flask(__name__)
chatbot = ChatBot()


@app.route("/")
def home():
    db = Database()
    posts = list(db.news.find().sort("_id", -1))
    return render_template("index.html", posts=posts)


@app.route("/run-agent", methods=["POST"])
def run_agent():
    try:
        initial_state = {
            "results": [],
            "posts": []
        }

        compiled_graph = graph.compile()
        compiled_graph.invoke(initial_state)

        return jsonify({"status": "success", "message": "Pipeline executed successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/chat", methods=["GET"])
def chat_page():
    return render_template("chat.html")


@app.route("/chat-api", methods=["POST"])
def chat_api():
    user_input = request.json.get("message")
    response = chatbot.chat(user_input)
    return jsonify({"response": response})

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)