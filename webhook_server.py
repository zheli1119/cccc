from flask import Flask, request, jsonify
from collections import deque

app = Flask(__name__)
BOT_TOKEN = "your_bot_token_here"  # 可选校验
queue = deque(maxlen=1000)  # 内存缓存，最多存 1000 条消息

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
