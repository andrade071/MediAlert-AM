from dotenv import load_dotenv
import os
import requests

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{token}/sendMessage"

dados = {
    "chat_id": chat_id,
    "text": "✅ Teste do MediAlert AM"
}

r = requests.post(url, data=dados)

print(r.status_code)
print(r.text)