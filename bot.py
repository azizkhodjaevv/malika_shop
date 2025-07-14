from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from tv_data import TVS, CURRENCY

# Formatlash funksiyasi 
def format_prices(brand):
    result = []
    models = TVS.get(brand, [])
    if not models:
        return "Ma'lumot topilmadi."
    
    result.append(f"*{brand} modellari:*")
    for tv in models:
        series = f" ({tv['series']})" if tv.get("series") else ""
        line = f"• `{tv['model']}` — *{tv['price']}* {CURRENCY}{series}"
        result.append(line)
    return "\n".join(result)

# /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tugmalar = [
        ["Samsung 📺", "LG 📺"],
        ["MOONX 📺", "SKYWORTH 📺"],
        ["RULLS 📺", "7TECH 📺"],
        ["IMMER 📺", "ZIFFLER 📺"],
        ["SONY 📺", "TOSHIBA 📺"],
        ["HISENSE 📺"]
    ]
    await update.message.reply_text(
        "Assalomu alaykum!\nQaysi televizor narxini ko‘rmoqchisiz?",
        reply_markup=ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
    )

# Tugmani bosganda javob qaytarish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    for brand in TVS:
        if brand.lower() in text:
            msg = format_prices(brand)
            await update.message.reply_markdown(msg)
            return
    await update.message.reply_text("Bunday brend topilmadi.")

# Botni ishga tushurish
app = ApplicationBuilder().token("8182175539:AAHTdi4ipR0lFLKw6nFqAvHxTR9H5Y0AdSU").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
