from flask import Flask, request
import requests
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def send_email(to_email):
    msg = MIMEText("This is an automated email from your Telegram bot.")
    msg["Subject"] = "Hello from your bot!"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

    return f"✅ Email sent to {to_email}!"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/email"):
            parts = text.split()
            if len(parts) == 2:
                recipient = parts[1]
                # Simple validation: check if it contains '@'
                if "@" in recipient:
                    result = send_email(recipient)
                else:
                    result = "❌ Invalid email address."
            else:
                result = "❌ Usage: /email recipient@example.com"
            send_telegram_message(chat_id, result)
        else:
            send_telegram_message(chat_id, "Send /email recipient@example.com to send an email.")

    return {"ok": True}

if __name__ == "__main__":
    app.run(debug=True)
