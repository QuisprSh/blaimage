import os
from dotenv import load_dotenv
import requests

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
APP_ID = os.getenv("DISCORD_APP_ID")

url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"
print(f"{url}")

payload = {
    "name": "blahaj",
    "description": "Get Blahaj images or stats",
    "options": [
        {
            "name": "action",
            "description": "Choose image or stats",
            "type": 3,  # STRING type
            "required": True,
            "choices": [
                {"name": "image", "value": "image"},
                {"name": "stats", "value": "stats"}
            ]
        }
    ],
    "integration_types": [1],
    "contexts": [0,1,2],
}

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

r = requests.post(url, headers=headers, json=payload)
print(r.status_code, r.text)
