import os
from flask import Flask, request, jsonify
from collections import deque

from dotenv import load_dotenv
load_dotenv()  # 本地调试用，Render上不影响

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("请设置环境变量 BOT_TOKEN")

queue = deque(maxlen=1000)  # 消息队列缓存，最多缓存1000条

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

if __name__ == "__main__":
    # 仅本地测试时用，Render 上用 gunicorn 启动
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
