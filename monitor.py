import time
import os
import requests

# 優先使用環境變數，否則使用硬編碼（方便 Render Debug）
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8142937859:AAFIRhDThncqUSaYH4hYOUZcNLFFDMvaDQk")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7398446407")

def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram TOKEN 或 CHAT_ID 環境變數未設置")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        res = requests.post(url, data=payload)
        print(f"📤 推播成功: {text} | Status: {res.status_code}")
    except Exception as e:
        print(f"⚠️ 推播失敗: {e}")

def run_monitor():
    send_telegram_message("✅ V27.3 策略已啟動，Telegram 通知測試成功！")
    while True:
        message = "🛡️ V27.3 策略正在監控中... 每10秒推播一次"
        print(message)
        send_telegram_message(message)
        time.sleep(10)

if __name__ == "__main__":
    run_monitor()

