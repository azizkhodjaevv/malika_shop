import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from tv_data import tv_data
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not set in environment variables!")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(brand, callback_data=brand)] for brand in tv_data.keys()
    ]
    keyboard.append([InlineKeyboardButton("📍 Joylashuv", url="https://maps.app.goo.gl/KabQXZCpkDq7B2Nw6")])
    keyboard.append([InlineKeyboardButton("📞 Aloqa", callback_data="contact")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Quyidagilardan birini tanlang:", reply_markup=reply_markup)

# Button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    brand = query.data
    if brand == "contact":
        await query.edit_message_text("📞 Aloqa: +998 90 123 45 67\n📍 Manzil: Malika Bozori, B20 do‘kon")
    elif brand in tv_data:
        tv_list = "\n".join([f"{model} — {price}" for model, price in tv_data[brand]])
        await query.edit_message_text(f"📺 {brand} narxlari:\n\n{tv_list}")
    else:
        await query.edit_message_text("Nomaʼlum buyruq!")

# Build application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Run
