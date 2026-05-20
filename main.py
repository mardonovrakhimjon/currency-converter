from datetime import datetime
import requests
import telebot
from telebot import types

# Bot tokeningiz
BOT_TOKEN = '8820173603:AAFPAN7SFxa2cXX1el2aHJWmv_q_RAJI4fI'
bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchi ma'lumotlarini vaqtincha saqlash uchun lug'at
user_data = {}

# Markaziy bankdan ma'lumot olish
def get_currency_data():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    response = requests.get(url)
    return response.json()

# Kursni aniqlash
def get_currency_rate(currency_code):
    data = get_currency_data()
    for item in data:
        if item['Ccy'] == currency_code:
            return float(item['Rate'])
    return None

# /start buyrug'i berilganda tugmalarni ko'rsatish
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('USD', 'EUR', 'RUB')
    
    msg = bot.send_message(
        message.chat.id, 
        "Salom! Valyuta ayboshlash botiga xush kelibsiz.\nQaysi valyutani tanlaysiz?", 
        reply_markup=markup
    )
    # Keyingi qadamga o'tish (valyutani tekshirish)
    bot.register_next_step_handler(msg, process_currency_step)

# Valyuta tanlangandan keyingi qadam
def process_currency_step(message):
    currency = message.text.upper()
    if currency in ['USD', 'EUR', 'RUB']:
        user_data[message.chat.id] = {'currency': currency}
        msg = bot.send_message(
            message.chat.id, 
            f"Qiymatni kiriting (Masalan: 100):",
            reply_markup=types.ReplyKeyboardRemove() # Tugmalarni yopish
        )
        # Keyingi qadamga o'tish (summani hisoblash)
        bot.register_next_step_handler(msg, process_amount_step)
    else:
        msg = bot.send_message(message.chat.id, "Iltimos, faqat tugmalardan birini tanlang (USD, EUR, RUB):")
        bot.register_next_step_handler(msg, process_currency_step)

# Summa kiritilgandan keyingi qadam va hisoblash
def process_amount_step(message):
    try:
        amount = float(message.text)
        chat_id = message.chat.id
        currency_code = user_data[chat_id]['currency']
        
        rate = get_currency_rate(currency_code)
        
        if rate is not None:
            converted_amount = amount * rate
            text = (
                f"📊 **Natija:**\n\n"
                f"{amount:,.2f} {currency_code} = {converted_amount:,.2f} UZS\n"
                f"Kurs: 1 {currency_code} = {rate:,.2f} UZS"
            )
            bot.send_message(chat_id, text, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "Xatolik: Valyuta kursi topilmadi.")
            
        # Qayta boshlash imkoniyati
        start_command(message)
        
    except ValueError:
        msg = bot.send_message(message.chat.id, "Iltimos, faqat son kiriting (Masalan: 50 yoki 12.5):")
        bot.register_next_step_handler(msg, process_amount_step)

# Botni ishga tushirish
if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling()
