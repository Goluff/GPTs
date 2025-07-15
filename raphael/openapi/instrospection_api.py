from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()
JOURNAL_FILE = "priscilla_journal.json"

# Chargement initial
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w") as f:
        json.dump({"entries": []}, f)

class JournalEntry(BaseModel):
    entry: str

@app.get("/journal/priscilla")
def get_journal():
    with open(JOURNAL_FILE, "r") as f:
        data = json.load(f)
    return {"entries": data["entries"]}

@app.post("/journal/priscilla")
def post_journal(entry: JournalEntry):
    with open(JOURNAL_FILE, "r") as f:
        data = json.load(f)
    data["entries"].append(entry.entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "ok"}
