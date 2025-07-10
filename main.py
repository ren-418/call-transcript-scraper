import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import json
import os
import uuid
from selenium_worker import scrape_transcript
import base64

app = FastAPI()

class CallData(BaseModel):
    closer_name: str
    closer_email:str
    date_of_call: str
    fathom_link: str
    lead_name: str

# Example FastAPI
@app.get("/ping")
def ping():
    print("call recevied")
    return {"status": "ok"}


@app.post("/webhook")
async def handle_webhook(request: Request):
    print("call recevied")
    payload = await request.json()
    try:
        data = payload["data"]
        closer_name = data["closer_name"]
        closer_email = data["closer_email"]
        date_of_call = data["date_of_call"]
        fathom_link = data["fathom_link"]
        lead_name = data["lead_name"]
    except Exception as e:
        print(f"❌ Invalid payload: {e}")
        return {"status": "error", "reason": str(e)}
    print(f"▶️ Received: {closer_name} {closer_email} | {fathom_link} | {date_of_call} | {lead_name}")
    job = {
        "closer_name": closer_name,
        "closer_email": closer_email,
        "date_of_call": date_of_call,
        "fathom_link": fathom_link
    }
    result = scrape_transcript(job)
    transcript_text = result["transcript_text"]
    
    if transcript_text is None:
        transcript_text = ""
    transcript_text_b64 = base64.b64encode(transcript_text.encode("utf-8")).decode("utf-8")
    response = {
        "closer_name": result["closer_name"],
        "closer_email": result["closer_email"],
        "transcript_text": transcript_text_b64,
        "transcript_link": fathom_link,
        "date_of_call": result["date_of_call"],
        "lead_name":lead_name
    }
    print("date of call", result["date_of_call"])
    if result.get("error"):
        response["error"] = result["error"]
    return response
