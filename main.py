from flask import Flask
import os
import threading
import monitor

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ V27.3 Guardian Strategy is Active."

if __name__ == "__main__":
    # 啟動策略邏輯為背景執行緒
    threading.Thread(target=monitor.run_monitor, daemon=True).start()
    
    # 啟動 Flask Web Server
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)