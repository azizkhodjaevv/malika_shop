from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import os

# TOKEN
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# TV narxlari (misol)
tv_prices = {
    "Samsung": "📺 Samsung TV narxlari:\n- 55” = 5,500,000 so'm\n- 65” = 7,000,000 so'm",
    "LG": "📺 LG TV narxlari:\n- 55” = 5,200,000 so'm\n- 65” = 6,800,000 so'm",
    "MOONX": "📺 MOONX TV narxlari:\n- 43” = 3,300,000 so'm\n- 50” = 3,900,000 so'm",
    "SKYWORTH": "📺 SKYWORTH TV narxlari:\n- 32” = 2,100,000 so'm\n- 43” = 2,900,000 so'm",
    "RULLS": "📺 RULLS TV narxlari:\n- 32” = 1,700,000 so'm\n- 43” = 2,600,000 so'm",
    "7TECH": "📺 7TECH TV narxlari:\n- 24” = 1,400,000 so'm\n- 32” = 1,850,000 so'm",
    "IMMER": "📺 IMMER TV narxlari:\n- 43” = 2,500,000 so'm\n- 55” = 3,900,000 so'm",
    "ZIFFLER": "📺 ZIFFLER TV narxlari:\n- 32” = 1,600,000 so'm\n- 40” = 2,100,000 so'm",
    "SONY": "📺 SONY TV narxlari:\n- 50” = 5,900,000 so'm\n- 65” = 8,300,000 so'm",
    "TOSHIBA": "📺 TOSHIBA TV narxlari:\n- 32” = 2,400,000 so'm\n- 43” = 3,300,000 so'm",
    "HISENSE": "📺 HISENSE TV narxlari:\n- 40” = 2,800,000 so'm\n- 50” = 3,600,000 so'm",
}

# Tugma yasash
def build_keyboard():
    buttons = [
        [InlineKeyboardButton(brand, callback_data=brand)] for brand in tv_prices.keys()
    ]
    return InlineKeyboardMarkup(buttons)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Televizor brendini tanlang 👇",
        reply_markup=build_keyboard()
    )

# Tugma bosilganda
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    brand = query.data
    prices = tv_prices.get(brand, "Ma'lumot topilmadi.")

    message = f"""📺 *{brand}* narxlari:\n{prices}

📞 [24/7: +998 97-188-33-30](tel:+998971883330)
📍 Manzil: [Toshkent, Malika Bozori B20](https://maps.app.goo.gl/UjkVEXPrnaGonokC7)
🚛 Yetkazib berish va o'rnatish xizmati mavjud.
"""

    await query.edit_message_text(message, reply_markup=build_keyboard(), parse_mode="Markdown")

# Run
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
