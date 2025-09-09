import os, uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.genai as genai
from flask import render_template
from google.genai import types
import logging

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

app=Flask(__name__)

CORS(app)  # enable frontend requests
client = genai.Client(api_key=API_KEY)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


MODEL = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = (
    "You are a helpful, concise Q&A chatbot. "
    "If the user asks for factual answers, be precise and include short examples when useful. "
    "If unsure, ask a brief clarifying question."
)



@app.route("/", methods=["GET"])
def home():
    print("hi")
    logger.debug("test")
    logger.debug("This is a debug message")

    return render_template("index.html")


import os, uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.genai as genai
from flask import render_template
from google.genai import types
import logging

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

app=Flask(__name__)

CORS(app)  # enable frontend requests
client = genai.Client(api_key=API_KEY)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


MODEL = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = (
    "You are a helpful, concise Q&A chatbot. "
    "If the user asks for factual answers, be precise and include short examples when useful. "
    "If unsure, ask a brief clarifying question."
)

def to_content(role, text):
    print(role)
    part = types.Part.from_text(text=text)
    content = types.Content(role=role, parts=[part])
    return content


@app.route("/", methods=["GET"])
def home():
    print("hi")
    logger.debug("test")
    logger.debug("This is a debug message")

    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_msg = data.get("message", "").strip()
    history = data.get("history", [])
    session = data.get("session") or str(uuid.uuid4())

    if not user_msg:
        return jsonify({"error": "message is required"}), 400

    contents = [to_content("model", SYSTEM_INSTRUCTION)]
    for m in history:
        if m.get("role") in ("user", "model") and m.get("content"):
            contents.append(to_content(m["role"], m["content"]))
    contents.append(to_content("user", user_msg))
    print(contents)
    # --- Gemini API Call ---
    resp = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(max_output_tokens=1024, temperature=0.6),
    )

    reply = (resp.text or "").strip()

    new_history = history + [
        {"role": "user", "content": user_msg},
        {"role": "model", "content": reply},
    ]

    return jsonify({"reply": reply, "history": new_history, "session": session})

if __name__ == "__main__":
    app.run(port=5050,debug=True)



# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()

#     user_msg = data.get("message", "").strip()
#     history = data.get("history", [])
#     session = data.get("session") or str(uuid.uuid4())

#     if not user_msg:
#         return jsonify({"error": "message is required"}), 400

#     contents = [to_content("system", SYSTEM_INSTRUCTION)]
#     for m in history:
#         if m.get("role") in ("user", "model") and m.get("content"):
#             contents.append(to_content(m["role"], m["content"]))
#     contents.append(to_content("user", user_msg))

#     # --- Gemini API Call ---
#     resp = client.models.generate_content(
#         model=MODEL,
#         contents=contents,
#         config=types.GenerateContentConfig(max_output_tokens=1024, temperature=0.6),
#     )

#     reply = (resp.text or "").strip()

#     new_history = history + [
#         {"role": "user", "content": user_msg},
#         {"role": "model", "content": reply},
#     ]

#     return jsonify({"reply": reply, "history": new_history, "session": session})

