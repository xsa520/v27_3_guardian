import os
import time
import threading
import requests
from flask import Flask

# 建立 Flask app 用來讓 Render 偵測此服務是否正常
app = Flask(__name__)

# 環境變數設定
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ====== 推播函數 ======
def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ 環境變數未正確設置")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print(f"📤 推播成功: {text}")
        else:
            print(f"⚠️ 推播失敗, status={res.status_code}, 回傳: {res.text}")
    except Exception as e:
        print(f"❗ 發送 Telegram 出錯: {e}")

# ====== 核心監控邏輯 ======
def run_monitor():
    send_telegram_message("✅ V27.3 策略已啟動，Telegram 通知測試成功！")
    while True:
        message = "🛡️ V27.3 策略正在監控中... 每10秒推播一次"
        print(message)
        send_telegram_message(message)
        time.sleep(10)

# ====== Flask 路由 (Render 健康檢查用途) ======
@app.route("/")
def index():
    return "🟢 V27.3 策略服務正在執行中"

# ====== 主執行區塊 ======
if __name__ == "__main__":
    # 背景執行 Telegram 推播
    threading.Thread(target=run_monitor, daemon=True).start()
    # 啟動 Flask Web 服務，Render 會透過這判斷服務存活
    app.run(host="0.0.0.0", port=10000)

