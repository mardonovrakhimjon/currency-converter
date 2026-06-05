import json
import os
import requests
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import settings

JSON_FILE = 'users.json'

def get_rate(currency_code):
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            for item in data:
                if item['Ccy'] == currency_code.upper():
                    return float(item['Rate'])
        except Exception:
            return None
    return None

def save_user(user_id, full_name):
    data = {}
    if os.path.exists(JSON_FILE):
        if os.path.getsize(JSON_FILE) > 0:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, dict):
                    data = loaded_data
                    
    data[str(user_id)] = {"full_name": full_name}
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def start(update, context):
    user = update.message.from_user
    save_user(user.id, user.full_name)
    
    buttons = [[KeyboardButton("📈 Valyuta kursi")]]
    update.message.reply_text(
        f"Salom, {user.full_name}! Botga xush kelibsiz.",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

def handle_message(update, context):
    text = update.message.text
    
    if text == "📈 Valyuta kursi":
        buttons = [[KeyboardButton("USD 🇺🇸"), KeyboardButton("EUR 🇪🇺"), KeyboardButton("RUB 🇷🇺")]]
        update.message.reply_text("Qaysi valyutani so'mga o'girmoqchisiz?", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return

    if text == "USD 🇺🇸":
        context.user_data['selected_currency'] = "USD"
        update.message.reply_text("Miqdorni kiriting (Faqat raqam):")
        return
    elif text == "EUR 🇪🇺":
        context.user_data['selected_currency'] = "EUR"
        update.message.reply_text("Miqdorni kiriting (Faqat raqam):")
        return
    elif text == "RUB 🇷🇺":
        context.user_data['selected_currency'] = "RUB"
        update.message.reply_text("Miqdorni kiriting (Faqat raqam):")
        return

    if 'selected_currency' in context.user_data:
        currency = context.user_data['selected_currency']
        clean_text = text.replace('.', '', 1)
        
        if clean_text.isdigit():
            amount = float(text)
            rate = get_rate(currency)
            
            if rate is not None:
                result = amount * rate
                buttons = [[KeyboardButton("📈 Valyuta kursi")]]
                update.message.reply_text(
                    f"📊 Natija: {amount:,.2f} {currency} = {result:,.2f} so'm\n"
                    f"📈 Kurs: 1 {currency} = {rate} so'm",
                    reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                )
            else:
                update.message.reply_text("Kurs ma'lumotlarini yuklashda xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.")
                
            del context.user_data['selected_currency']
        else:
            update.message.reply_text("Iltimos, faqat raqam yuboring!")

updater = Updater(settings.TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

print("Bot faol...")
updater.start_polling()
updater.idle()
