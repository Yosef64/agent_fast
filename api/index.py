from http import HTTPStatus
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler
from telegram.ext._contexttypes import ContextTypes
from fastapi import FastAPI, Request, Response


app = FastAPI()
async def start(update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Visit Web App", web_app={"url": "https://victory-contest.vercel.app/"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click the button below to visit our web app.", reply_markup=reply_markup)
@app.post("/")
async def process_update(request: Request):
    ptb = (
    Application.builder()
    .updater(None)
    .token("7897490261:AAFMKWSSK0wHuSHlROpQH5WW9v4VsSTlkoA") 
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
   )
    await ptb.initialize()
    ptb.add_handler(CommandHandler("start", start))
    req = await request.json()
    
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)
@app.get("/")
def index(request:Request):
    return {"message": "Hello World"}

#https://victory-fast.vercel.app/
# https://api.telegram.org/bot7897490261:AAFMKWSSK0wHuSHlROpQH5WW9v4VsSTlkoA/setWebhook?url=https://victory-fast.vercel.app/
# 
