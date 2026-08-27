from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

class Lead(BaseModel):
    name: str
    contact: str
    store: str
    store_other: str = ""
    pain: str
    comment: str = ""

@app.post("/api/lead")
async def submit_lead(lead: Lead):
    # Токены берутся из переменных окружения Vercel
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")

    store_line = lead.store
    if lead.store == "Другое" and lead.store_other:
        store_line = f"Другое ({lead.store_other})"

    comment_line = lead.comment if lead.comment else "—"

    text = (
        f"🔥 Новая заявка в Racio!\n\n"
        f"👤 Имя: {lead.name}\n"
        f"📞 Контакт: {lead.contact}\n"
        f"🛒 Магазин: {store_line}\n"
        f"🎯 Что раздражает: {lead.pain}\n"
        f"💬 Комментарий: {comment_line}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"chat_id": CHAT_ID, "text": text})

    if response.status_code == 200:
        return {"status": "success"}
    return {"status": "error", "details": response.text}
