from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler
from telegram.ext._contexttypes import ContextTypes
from fastapi import FastAPI, Request, Response
# from dbActions import askPayment, getUserStatById,registerAgent,getUserById,getOwnAgent


app = FastAPI()

def getReplyMarkUp():
    keyboard = [
        ["📝 ለኤጀንት ምዝገባ", "🔗 Referral link ለማግኘት"],
        ["💰 ብር ለማውጣት","📊 በስራቹ የገቡ የተማሪዎች ብዛት"],
        ["💵 ቀሪ ሂሳብ ለማወቅ","🔢 በኤጀንቶቻቹ የገቡ የተማሪዎች ብዛት"],
        ["በስራቹ የተመዘገቡ ኤጀንቶች ብዛት"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    return reply_markup
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = getReplyMarkUp()
    
    await update.message.reply_text(
        "Hello biach",reply_markup=reply_markup
    )

@app.post("/")
async def process_update(request: Request):
    ptb = (
    Application.builder()
    .updater(None)
    .token("7756252447:AAH6fSVh8Q6s2hip4w4wCblqDuOtrLSWSR4") 
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
# https://api.telegram.org/bot7756252447:AAH6fSVh8Q6s2hip4w4wCblqDuOtrLSWSR4/setWebhook?url=https://agent-fast.vercel.app
# https://api.telegram.org/bot7756252447:AAH6fSVh8Q6s2hip4w4wCblqDuOtrLSWSR4/setWebhook?url=https://victoryagentbotfastapi.vercel.app/
# 
# 
