import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from tv_data import tv_prices

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN not set in environment variables!")

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(brand, callback_data=brand)]
        for brand in tv_prices.keys()
    ]
    keyboard.append([InlineKeyboardButton("📍 Manzil", callback_data="location")])
    keyboard.append([InlineKeyboardButton("📞 Aloqa", callback_data="contact")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Quyidagi brendni tanlang:", reply_markup=reply_markup)

# Tugma bosilganda ishlovchi funksiyalar
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "location":
        await query.edit_message_text("📍 Manzil: Malika Bozori, B20 do‘kon")
    elif data == "contact":
        await query.edit_message_text("📞 Aloqa: +998 99 123 45 67")
    elif data in tv_prices:
        tv_list = "\n".join(tv_prices[data])
        await query.edit_message_text(f"🖥 {data} televizor narxlari:\n\n{tv_list}")
    else:
        await query.edit_message_text("Noma'lum tanlov.")

# Botni ishga tushurish
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    app.run_polling()
