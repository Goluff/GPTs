
from fastapi import FastAPI, Request, HTTPException
import hashlib, hmac, os
from typing import Dict
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Clé API secrète et clé HMAC (à stocker en variables d'environnement en production)
API_KEY = "your-api-key-here"
HMAC_SECRET = b"your-hmac-secret"

class Record(BaseModel):
    user_id: str
    date: str
    category: str
    score: int
    note: str

# Stockage en mémoire (à remplacer par une vraie BDD)
DATA = {}

def verify_signature(signature: str, body: bytes):
    computed = hmac.new(HMAC_SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, computed)

@app.post("/record_entry")
async def record_entry(request: Request):
    headers = request.headers
    api_key = headers.get("X-API-Key")
    signature = headers.get("X-Signature")

    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    body = await request.body()
    if not verify_signature(signature, body):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    user_id = payload["user_id"]
    date = payload["date"]
    if user_id not in DATA:
        DATA[user_id] = {}
    DATA[user_id][date] = {
        "category": payload["category"],
        "score": payload["score"],
        "note": payload["note"]
    }
    return {"message": "Data recorded", "entries": len(DATA[user_id])}

@app.get("/retrieve_history")
def retrieve_history(user_id: str, category: str = None):
    if user_id not in DATA:
        return {}

    history = {
        date: entry["score"]
        for date, entry in DATA[user_id].items()
        if category is None or entry["category"] == category
    }
    return history

@app.delete("/delete_session")
def delete_session(user_id: str):
    if user_id in DATA:
        del DATA[user_id]
        return {"status": "deleted"}
    return {"status": "no data"}
