from flask import Flask, request
import os
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

def send_email():
    msg = MIMEText("This is an automated email from your Telegram bot.")
    msg["Subject"] = "Hello from your bot!"
    msg["From"] = SMTP_EMAIL
    msg["To"] = SMTP_EMAIL  # You can replace with any recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

    return "✅ Email sent!"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    if text.strip() == "/email":
        result = send_email()
        send_telegram_message(chat_id, result)

    return "OK"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "Bot is live."

if __name__ == "__main__":
    app.run()
