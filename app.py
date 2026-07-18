import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from utils.Graph import graph, is_invalid_generated_post
from utils.database import Database
from utils.chatbot import ChatBot

load_dotenv()

app = Flask(__name__)
chatbot = ChatBot()
MAX_AGENT_RUNS = 3
INITIAL_POST_LIMIT = 9
POST_PAGE_SIZE = 9


def serialize_post(post):
    return {
        "title": post.get("title", ""),
        "content": post.get("content", ""),
        "topic": post.get("topic", ""),
        "source_url": post.get("source_url", "#"),
        "image": post.get("image")
    }


@app.route("/")
def home():
    db = Database()
    posts = db.get_latest_posts(limit=INITIAL_POST_LIMIT)
    total_posts = db.count_posts()
    return render_template(
        "index.html",
        posts=posts,
        total_posts=total_posts,
        initial_post_limit=INITIAL_POST_LIMIT,
        post_page_size=POST_PAGE_SIZE
    )


@app.route("/api/posts")
def get_posts():
    try:
        offset = max(int(request.args.get("offset", 0)), 0)
        limit = min(max(int(request.args.get("limit", POST_PAGE_SIZE)), 1), 24)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid pagination parameters"}), 400

    db = Database()
    posts = [serialize_post(post) for post in db.get_latest_posts(limit=limit, skip=offset)]
    total_posts = db.count_posts()
    return jsonify({
        "posts": posts,
        "total": total_posts,
        "offset": offset,
        "limit": limit,
        "has_more": offset + len(posts) < total_posts
    })


@app.route("/run-agent", methods=["POST"])
def run_agent():
    try:
        compiled_graph = graph.compile()
        last_state = None

        for attempt in range(1, MAX_AGENT_RUNS + 1):
            initial_state = {
                "results": [],
                "posts": []
            }

            last_state = compiled_graph.invoke(initial_state)
            posts = last_state.get("posts", []) if last_state else []
            valid_posts = [post for post in posts if not is_invalid_generated_post(post)]

            if valid_posts:
                return jsonify({
                    "status": "success",
                    "message": "Pipeline executed successfully",
                    "attempts": attempt
                })

        return jsonify({
            "status": "error",
            "message": "Pipeline returned only invalid articles after retries",
            "attempts": MAX_AGENT_RUNS,
            "last_posts": last_state.get("posts", []) if last_state else []
        }), 502
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

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
