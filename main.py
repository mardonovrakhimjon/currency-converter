import json
import requests
from settings import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler
from telegram.utils.request import Request

def valyuta_kursini_ol(valyuta_kodi):
    url = f"https://cbu.uz{valyuta_kodi}/"
    
    response = requests.get(url, timeout=5)
    data = response.json()
    
    kurs_info = data[0] if isinstance(data, list) else data
    return kurs_info

def send_welcome(update, context):
    keyboard = [
        [
            KeyboardButton(text="Bosh Sahifa"),
            KeyboardButton(text="Mahsulotlar"),
            KeyboardButton(text="Valyuta Kursi")
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    matn = (
        " Welcome!\n\n"
        "I am a bot that shows the latest exchange rates of the Central Bank.\n"
        "Send the /kurs command to see the exchange rates."
    )
    update.message.reply_text(text=matn, reply_markup=reply_markup)


def send_rates(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    valyutalar = ['USD', 'EUR', 'RUB']
    javob_matni = "**Central Bank Exchange Rates:**\n\n"
    sana = ""
    
    for kod in valyutalar:
        info = valyuta_kursini_ol(kod)
        javob_matni += f"🔹 1 **{info['Ccy']}** = {info['Rate']} UZS ({info['CcyNm_EN']})\n"
        sana = info['Date']
            
    javob_matni += f"\n *Date:* {sana}"
    update.message.reply_text(javob_matni, parse_mode='Markdown')

def main():
    updater = Updater(token=settings.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['start', 'help'], send_welcome))
    dispatcher.add_handler(CommandHandler('kurs', send_rates))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

def save_user(update):
    if not update.message or not update.message.from_user:
        return
        
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name

    file = open("users.json", "r", encoding="utf-8")
    users = json.load(file)
    file.close()

    exists = False
    for u in users:
        if u["user_id"] == user_id:
            exists = True

    if not exists:
        new_user = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name
        }
        users.append(new_user)
        
        file = open("users.json", "w", encoding="utf-8")
        json.dump(users, file, indent=4, ensure_ascii=False)
        file.close()

def start_funksiyasi(message):
    
    save_user(message.from_user.id, message.from_user.username, message.from_user.first_name)

if __name__ == "__main__":
    main()
