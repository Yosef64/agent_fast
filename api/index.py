from http import HTTPStatus
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler,MessageHandler,CallbackQueryHandler,filters,CallbackContext
from telegram.ext._contexttypes import ContextTypes
from fastapi import FastAPI, Request, Response


app = FastAPI()
async def start(update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Visit Web App", web_app={"url": "https://victory-contest.vercel.app/"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click the button below to visit our web app.", reply_markup=reply_markup)
async def options(update,_,context:CallbackContext):
    text = update.message.text
    # if text == "🔢 በኤጀንቶቻቹ የገቡ የተማሪዎች ብዛት":
    #     await 
    # elif text == "📝 ለኤጀንት ምዝገባ":
    #     await register(update,context)
    # elif text == "💰 ብር ለማውጣት":
    #     await payMe(update,context)
    # elif text == "🔗 Referral link ለማግኘት":
    #     await getLinks(update,context)
    # elif text == "💵 ቀሪ ሂሳብ ለማወቅ":
    #     await getAmount(update,context)
    # elif text == "📊 በስራቹ የገቡ የተማሪዎች ብዛት":
    #     await getNumberOfStud(update,context)
    # elif text == "በስራቹ የተመዘገቡ ኤጀንቶች ብዛት":
    #     await ownAgent(update,context)
    await update.message.reply_text(text)
# async def button(update:_,context:CallbackContext):
#     query = update.callback_query
#     await query.answer()
#     if query.data == "1":
#         await query.
#     elif query.data == "2":
#         await getStudentReferral(update,context)
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
    ptb.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,options))
    # ptb.add_handler(CallbackQueryHandler(button))
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
