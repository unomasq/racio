from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

class Lead(BaseModel):
    name: str
    contact: str
    store: str
    goal: str

@app.post("/api/submit-lead")
async def submit_lead(lead: Lead):
    # Токены берутся из переменных окружения Vercel
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")
    
    text = f"🔥 Новая заявка в Racio!\n\n👤 Имя: {lead.name}\n📞 Контакт: {lead.contact}\n🛒 Магазин: {lead.store}\n🎯 Цель: {lead.goal}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"chat_id": CHAT_ID, "text": text})
        
    if response.status_code == 200:
        return {"status": "success"}
    return {"status": "error", "details": response.text}
