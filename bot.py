from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from tv_data import tv_prices
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8182175539:AAFrI70ITVYjbdguULzULEymHj1yV_0H6MY")

# Tugmalar yasash
def build_keyboard():
    keyboard = [[InlineKeyboardButton(brand, callback_data=brand)] for brand in tv_prices.keys()]
    return InlineKeyboardMarkup(keyboard)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📺 Malika bozori B20 do'kondagi televizor narxlari botiga xush kelibsiz!\n\n"
        "Quyidagi brendlardan birini tanlang:",
        reply_markup=build_keyboard()
    )

# Tugma bosilganda
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    brand = query.data
    prices = tv_prices.get(brand, "Ma'lumot topilmadi.")

    message = f"""📦 *{brand} narxlari:*

{prices}

📍 [Toshkent, Malika bozori B20 do‘kon](https://maps.app.goo.gl/UjkVEXPrnaGonokC7)

📞 [24/7: +998 97-188-33-30](tel:+998971883330)
🚚 Shahar bo‘ylab yetkazib berish xizmati mavjud
🛠️ O‘rnatib berish xizmati ham mavjud
"""

    await query.edit_message_text(text=message, parse_mode="Markdown", reply_markup=build_keyboard())

# Botni ishga tushurish
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()
