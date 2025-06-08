import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import httpx

load_dotenv()

API_URL = os.getenv("API_URL")
DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

app = FastAPI()

# Discord interaction types
PING = 1
APPLICATION_COMMAND = 2
CHANNEL_MESSAGE_WITH_SOURCE = 4

# Verify Discord request signature
def verify_signature(request: Request, body: bytes):
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    if not signature or not timestamp:
        return False

    import nacl.signing
    import nacl.exceptions

    message = timestamp.encode() + body
    try:
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY)) # type: ignore
        verify_key.verify(message, bytes.fromhex(signature))
        return True
    except nacl.exceptions.BadSignatureError:
        return False


@app.post("/interactions")
async def interactions(request: Request):
    body = await request.body()

    if not verify_signature(request, body):
        raise HTTPException(status_code=401, detail="Invalid request signature")

    payload = json.loads(body)

    if payload["type"] == PING:
        return JSONResponse({"type": 1})

    if payload["type"] == APPLICATION_COMMAND:
        data = payload["data"]
        if data["name"] == "blahaj":
            options = data.get("options", [])
            action = None
            for opt in options:
                if opt["name"] == "action":
                    action = opt["value"]

            if action == "image":
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{API_URL}/")
                    resp.raise_for_status()
                    result = resp.json()
                url = result.get("url")
                if not url:
                    return JSONResponse({
                        "type": CHANNEL_MESSAGE_WITH_SOURCE,
                        "data": {"content": "Sorry, no image found."}
                    })
                return JSONResponse({
                    "type": CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {
                        "embeds": [{
                            "image": {"url": url},
                            "title": "Here's your Blahaj image!"
                        }]
                    }
                })

            elif action == "stats":
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{API_URL}/stats")
                    resp.raise_for_status()
                    result = resp.json()
                count = result.get("file_count")
                if count is None:
                    return JSONResponse({
                        "type": CHANNEL_MESSAGE_WITH_SOURCE,
                        "data": {"content": "Sorry, stats not found."}
                    })
                return JSONResponse({
                    "type": CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {
                        "content": f"There are {count} images in the api (provided by {API_URL })!",
                        "flags": 64  # ephemeral message
                    }
                })
            else:
                return JSONResponse({
                    "type": CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {"content": "Unknown action. Use image or stats."}
                })

    return JSONResponse({"type": 4, "data": {"content": "Command not recognized"}})
