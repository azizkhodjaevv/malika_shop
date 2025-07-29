from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from tv_data import tv_prices

# Telegram bot tokeningiz
TELEGRAM_TOKEN = "8182175539:AAFrI70ITVYjbdguULzULEymHj1yV_0H6MY"

# Brend tugmalarini qurish
def build_keyboard():
    brands = list(tv_prices.keys())

    keyboard = [
        [InlineKeyboardButton(brands[i], callback_data=brands[i]),
         InlineKeyboardButton(brands[i + 1], callback_data=brands[i + 1])]
        for i in range(0, len(brands) - 1, 2)
    ]

    if len(brands) % 2 != 0:
        keyboard.append([InlineKeyboardButton(brands[-1], callback_data=brands[-1])])

    keyboard.append([InlineKeyboardButton("📍 Manzilni ko‘rish", callback_data="location")])

    return InlineKeyboardMarkup(keyboard)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = build_keyboard()
    await update.message.reply_text("📺 Televizor brendini tanlang:", reply_markup=reply_markup)

# Tugma bosilganda ishlovchi funksiyalar
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "location":
        # Malika bozor, B20 do‘kon koordinatalari
        latitude = 41.300312
        longitude = 69.250252

        await query.message.reply_location(latitude=latitude, longitude=longitude)

        await query.message.reply_text(
            "📍 Toshkent shahar, Malika bozor, B20 do‘kon\n\n"
            "Agar topa olmasangiz yoki yordam kerak bo‘lsa:\n"
            "📞 [24/7: +998 97-188-33-30](tel:+998971883330)",
            parse_mode="Markdown"
        )
        return

    # Brendga tegishli narxlar
    prices = tv_prices.get(data, "Ma'lumot topilmadi.")

    message = f"""📦 {data} narxlari:

{prices}

📞 [24/7: +998 97-188-33-30](tel:+998971883330)
🚚 Shahar bo'yicha yetkazib berish (dastavka) mavjud
🛠 O'rnatib berish xizmati ham mavjud
"""

    reply_markup = build_keyboard()
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")

# Botni ishga tushirish
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
