python
from flask import Flask
from threading import Thread
import requests
import time
‌
# --- بخش بیدار نگه داشتن سرور برای Render ---
app = Flask('')
‌
@app.route('/')
def home():
return "I'm alive!"
‌
def run():
# Render معمولاً پورت 10000 را استفاده می‌کند
app.run(host='0.0.0.0', port=10000)
‌
# اجرای سرور در یک رشته (Thread) جداگانه تا ربات همزمان اجرا شود
Thread(target=run).start()
‌
# --- تنظیمات ربات بله ---
# توکن شما با موفقیت جایگزین شد
TOKEN = "999634402:BcvIyQmMol5pFf_FtgcmAkUQQgFYP1-G9Wg"
BALE_API_URL = "https://t.bale.ai"
‌
def get_updates(offset=None):
url = f"{BALE_API_URL}/getUpdates"
params = {"offset": offset, "timeout": 30}
try:
response = requests.get(url, params=params, timeout=31)
return response.json()
except Exception as e:
print(f"Error fetching updates: {e}")
return None
‌
def send_message(chat_id, text):
url = f"{BALE_API_URL}/sendMessage"
payload = {"chat_id": chat_id, "text": text}
try:
requests.post(url, json=payload)
except Exception as e:
print(f"Error sending message: {e}")
‌
def main():
print("Bot is starting...")
offset = None
while True:
updates = get_updates(offset)
if updates and "ok" in updates and updates["ok"]:
for update in updates["result"]:
offset = update["update_id"] + 1
‌
if "message" in update:
chat_id = update["message"]["chat"]["id"]
text = update["message"].get("text", "")
‌
# پاسخ‌های ساده ربات
if text == "/start":
send_message(chat_id, "سلام! من ربات شما هستم که روی Render اجرا می‌شوم. 👁️🤘")
elif text == "سلام":
send_message(chat_id, "سلام علیکم! چطور می‌توانم کمکت کنم؟")
else:
send_message(chat_id, f"شما گفتی: {text}")
‌
time.sleep(1)
‌
if __name__ == "__main__":
main()
