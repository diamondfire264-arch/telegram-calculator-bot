import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

def get_keyboard():
    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C"]
    ]
    keyboard = []
    for row in buttons:
        keyboard.append([InlineKeyboardButton(btn, callback_data=btn) for btn in row])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = ""
    await update.message.reply_text(
        "🧮 Calculator Ready\n\n0",
        reply_markup=get_keyboard()
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    expr = user_data.get(user_id, "")

    if data == "C":
        expr = ""
    elif data == "=":
        try:
            result = str(eval(expr))
            expr = result
        except:
            expr = "Error"
    else:
        expr += data

    user_data[user_id] = expr

    text = f"🧮 Calculator\n\n{expr if expr else 0}"

    await query.answer()
    await query.edit_message_text(text, reply_markup=get_keyboard())

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))

app.run_polling()
