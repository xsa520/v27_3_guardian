import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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
            print(f"⚠️ 推播失敗: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"❗ 發送 Telegram 出錯: {e}")

def run_monitor():
    send_telegram_message("✅ V27.3 策略已啟動，Telegram 通知測試成功！")
    while True:
        message = "🛡️ V27.3 策略正在監控中... 每10秒推播一次"
        print(message)
        send_telegram_message(message)
        time.sleep(10)

@app.before_first_request
def activate_monitor_thread():
    threading.Thread(target=run_monitor, daemon=True).start()

@app.route("/")
def index():
    return "🟢 V27.3 策略服務已啟動，Flask 正常運行中"

