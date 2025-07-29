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

if not TELEGRAM_TOKEN:
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

# Tugma bosilganda ishlovchi funksiya
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "location":
        await query.edit_message_text("📍 Manzil: [Toshkent, Malika bozori B20 do‘kon](https://maps.app.goo.gl/UjkVEXPrnaGonokC7)", parse_mode="Markdown")
    elif data == "contact":
        await query.edit_message_text("📞 Aloqa: +998 97-188-33-30\n📦 Yetkazib berish va o‘rnatish xizmati mavjud")
    elif data in tv_prices:
        prices = "\n".join(tv_prices[data])
        await query.edit_message_text(
            f"📺 *{data} narxlari:*\n\n{prices}\n\n📍 [Manzil](https://maps.app.goo.gl/UjkVEXPrnaGonokC7)\n📞 [Aloqa](tel:+998971883330)",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("Noto‘g‘ri tanlov.")

# Botni ishga tushurish
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot ishga tushdi...")
    app.run_polling()
