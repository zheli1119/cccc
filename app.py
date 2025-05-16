import os
from flask import Flask, request, jsonify
from fastapi import FastAPI
from collections import deque

from dotenv import load_dotenv
load_dotenv()  # 本地调试用，Render 环境忽略

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("请设置环境变量 BOT_TOKEN")

queue = deque(maxlen=1000)  # 缓存最多1000条消息

@app.route(f"/bot{BOT_TOKEN}", methods=["POST"])
def receive_update():
    data = request.get_json()
    if data:
        queue.append(data)
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "no data"}), 400

@app.route("/get-updates", methods=["GET"])
def get_updates():
    updates = list(queue)
    queue.clear()
    return jsonify({"updates": updates})

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
