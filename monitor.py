import os
import time
import threading
import requests
from flask import Flask

# 建立 Flask App
app = Flask(__name__)

# 從環境變數讀取 Telegram 設定
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    print(f"⚙️ 正在準備推播：{text}")  # 顯示在 Render Logs
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram 環境變數未設置")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print("📤 推播成功")
        else:
            print(f"⚠️ 推播失敗，狀態碼: {res.status_code}，回應: {res.text}")
    except Exception as e:
        print(f"❗ 發送錯誤：{e}")

def run_monitor():
    send_telegram_message("✅ V27.3 策略已啟動，Telegram 通知測試成功！")
    while True:
        msg = "🛡️ V27.3 策略監控中，每10秒推播一次"
        send_telegram_message(msg)
        time.sleep(10)

@app.before_first_request
def launch_monitor():
    print("🚀 Flask 啟動，後台執行推播邏輯")
    threading.Thread(target=run_monitor, daemon=True).start()

@app.route("/")
def index():
    return "🟢 V27.3 Render 監控服務運行中"
