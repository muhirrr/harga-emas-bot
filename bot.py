import time
import requests
from datetime import datetime
from config import TELEGRAM_TOKEN, CHAT_ID, NOTIFY_URL
import logging

logging.basicConfig(level=logging.INFO)

def get_gold_price():
    try:
        response = requests.get("https://api.tokokiloe.com/emas")
        if response.status_code == 200:
            data = response.json()
            harga = data.get("price", {}).get("buy", 0)
            return harga
    except Exception as e:
        logging.error(f"Error fetching price: {e}")
    return None

def save_price(price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("harga_emas_log.txt", "a") as f:
        f.write(f"{now}, {price}\n")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

def send_notify(text):
    try:
        requests.post(NOTIFY_URL, data=text.encode("utf-8"))
    except Exception as e:
        logging.error(f"Error sending Notify.run: {e}")

def main_loop():
    while True:
        price = get_gold_price()
        if price:
            message = f"Harga emas per gram: Rp{price:,}"
            save_price(price)
            send_telegram_message(message)
            send_notify(message)
        time.sleep(3600)

if __name__ == "__main__":
    main_loop()
