from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler,CallbackQueryHandler,MessageHandler,filters,CallbackContext
from telegram.ext._contexttypes import ContextTypes
from fastapi import FastAPI, Request, Response
from dbActions import askPayment, getUserStatById,registerAgent,getUserById,getOwnAgent


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
async def getAgentReferal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.callback_query.from_user.id)  # Get user ID from the callback query
    stat,userRef = getUserStatById(user_id)

    if stat and stat["ownStud"] >= 2:
        await update.callback_query.message.reply_text(f"Your referral link is https://t.me/victory_t_est_bot?start={userRef}")
        return
    elif userRef:
        await update.callback_query.message.reply_text("ሁለት ሰው እና ከሁለት ሰው በላይ ማስገባት አለብህ!")
        return

    await update.callback_query.message.reply_text(f"You haven't registered as an agent yet! \nTo register -> /register")
    return

async def getStudentReferral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userRef = getUserById(str(update.callback_query.from_user.id))
    if userRef:
        await update.callback_query.message.reply_text(f"Your Student referral link is: https://t.me/victoryacademy_Bot?start={userRef}")
        return
    await update.callback_query.message.reply_text("You haven't registered Yet! You have to register to get referral link!")
    return
async def getLinks(update:Update,context:ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Get Agent Referral Link", callback_data='1')],
        [InlineKeyboardButton("Get Student Referral Link", callback_data='2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Now You have to choose which referral like. which means the referral link to let another student join or to add an agent under your side",reply_markup=reply_markup)
async def button(update:Update,context:CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == "1":
        await getAgentReferal(update,context)
    elif query.data == "2":
        await getStudentReferral(update,context)
async def getAmount(update:Update,context:ContextTypes.DEFAULT_TYPE):
    stat , _ =  getUserStatById(str(update.message.from_user.id))
    if stat:
        curAmount = stat["totalAmount"]
        await update.message.reply_text(f"Your current Amount is : {curAmount}")
        return
    await update.message.reply_text(f"You haven't registered yet! Press /start button to register")
    return
async def getNumberOfStud(update:Update,context:ContextTypes.DEFAULT_TYPE):
    stat,_ = getUserStatById(str(update.message.from_user.id))
    if stat:
        numStud = stat["ownStud"]
        await update.message.reply_text(f"You referred {numStud} students. Keep the great work!")
        return
    await update.message.reply_text("You haven't registered yet! press the register button to register!")
async def getNumberOfTeamStud(update:Update,context:ContextTypes):
    try:
        stat,ref = getUserStatById(str(update.message.from_user.id))
        if stat:
            numTeamStud = stat["agentStud"]
            await update.message.reply_text(f"You are in a team with {numTeamStud} students. Keep the great work!")
            return
        await update.message.reply_text("You haven't registered yet! press the register button to register.")
    except Exception as e:
        await update.message.reply_text("There was an error trying to get the numbers. Please try again!")
    return
async def payMe(update:Update,context:ContextTypes.DEFAULT_TYPE):
    isRegistered , asked,insuf = askPayment(str(update.message.from_user.id))
    if isRegistered and asked:
        await update.message.reply_text("Thanks for asking a payment for work! Our team will send the money and contact you as soon as possible. Wait patiently!")
    elif isRegistered and not asked:
        if insuf:
            await update.message.reply_text("Insufficient balance. Please add more students to receive payment.")
        else:
            await update.message.reply_text("You already sent a request for payment. Please wait patiently!")
    else:
        await update.message.reply_text("You haven't registered yet! Press the /register button to register.")
    return update.message.reply_text("There was an error trying to get the numbers. Please try again!")
async def ownAgent(update:Update,context:CallbackContext):
    userRef = getUserById(str(update.message.from_user.id))
    if not userRef:
        await update.message.reply_text("You haven't registered yet! please register first.")
        return
    agents = getOwnAgent(userRef)
    await update.message.reply_text(f"{agents} are registered under you!")
    return
async def register(update:Update,context:ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Register/ለመመዝገብ", web_app={"url": "https://victory-contest.vercel.app/"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("You can register by pressing the button below!", reply_markup=reply_markup)
async def options(update:Update,context:CallbackContext):
    text = update.message.text
    if text == "🔢 በኤጀንቶቻቹ የገቡ የተማሪዎች ብዛት":
        await getNumberOfTeamStud(update,context)
    elif text == "📝 ለኤጀንት ምዝገባ":
        await register(update,context)
    elif text == "💰 ብር ለማውጣት":
        await payMe(update,context)
    elif text == "🔗 Referral link ለማግኘት":
        await getLinks(update,context)
    elif text == "💵 ቀሪ ሂሳብ ለማወቅ":
        await getAmount(update,context)
    elif text == "📊 በስራቹ የገቡ የተማሪዎች ብዛት":
        await getNumberOfStud(update,context)
    elif text == "በስራቹ የተመዘገቡ ኤጀንቶች ብዛት":
        await ownAgent(update,context)

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
    ptb.add_handler(CallbackQueryHandler(button))
    req = await request.json()
    
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)
@app.get("/")
def index(request:Request):
    return {"message": "Hello World"}
@app.post("/register")
async def register(request:Request):
    
    data = await request.json()
    try:
        registerAgent(data,"133thhtht")
        return {"message":"ok"}
    except Exception as e:
        return {"message":e}
#https://victory-fast.vercel.app/
# https://api.telegram.org/bot7756252447:AAH6fSVh8Q6s2hip4w4wCblqDuOtrLSWSR4/setWebhook?url=https://agent-fast.vercel.app
# https://api.telegram.org/bot7756252447:AAH6fSVh8Q6s2hip4w4wCblqDuOtrLSWSR4/setWebhook?url=https://victoryagentbotfastapi.vercel.app/
# 
# 
