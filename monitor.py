import time
import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_USER_ID:
        print("❌ Telegram 環境變數未設置")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
        print(f"📤 推播成功: {text}")
    except Exception as e:
        print(f"⚠️ 推播失敗: {e}")

def run_monitor():
    while True:
        message = "🛡️ V27.3 策略正在監控中... 每10秒推播一次"
        print(message)
        send_telegram_message(message)
        time.sleep(10)