import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import json
import os
import uuid
from selenium_worker import scrape_transcript

app = FastAPI()

class CallData(BaseModel):
    closer_name: str
    closer_email:str
    date_of_call: str
    fathom_link: str

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    try:
        data = payload["data"]
        closer_name = data["closer_name"]
        closer_email = data["closer_email"]
        date_of_call = data["date_of_call"]
        fathom_link = data["fathom_link"]
    except Exception as e:
        print(f"❌ Invalid payload: {e}")
        return {"status": "error", "reason": str(e)}
    print(f"▶️ Received: {closer_name} {closer_email} | {fathom_link}")
    job = {
        "closer_name": closer_name,
        "closer_email": closer_email,
        "date_of_call": date_of_call,
        "fathom_link": fathom_link
    }
    result = scrape_transcript(job)
    response = {
        "closer_name": result["closer_name"],
        "closer_email": result["closer_email"],
        "transcript_text": result["transcript_text"],
        "date_of_call": result["date_of_call"]
    }
    print("result", result)
    if result.get("error"):
        response["error"] = result["error"]
    return response
