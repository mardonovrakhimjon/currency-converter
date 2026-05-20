import requests
import telebot

# Telegram bot tokenini shu yerga yozing
BOT_TOKEN = '8820173603:AAFPAN7SFxa2cXX1el2aHJWmv_q_RAJI4fI'
bot = telebot.TeleBot(BOT_TOKEN)

def valyuta_kursini_ol(valyuta_kodi):
    url = f"https://cbu.uz{valyuta_kodi}/"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Kelgan ma'lumot formatini tekshirish
        kurs_info = data[0] if isinstance(data, list) else data
        return kurs_info
    except Exception as e:
        print(f"API Xatolik: {e}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    matn = (
        "👋 Assalomu alaykum!\n\n"
        "Men Markaziy Bankning eng oxirgi valyuta kurslarini ko'rsatuvchi botman.\n"
        "Kurslarni bilish uchun /kurs buyrug'ini yuboring."
    )
    bot.reply_to(message, matn)

@bot.message_handler(commands=['kurs'])
def send_rates(message):
    # Bot foydalanuvchiga "yozmoqda..." holatini ko'rsatadi
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Kerakli valyutalarni ro'yxatdan o'tkazamiz
    valyutalar = ['USD', 'EUR', 'RUB']
    javob_matni = "💰 **Markaziy Bank valyuta kurslari:**\n\n"
    sana = ""

    for kod in valyutalar:
        info = valyuta_kursini_ol(kod)
        if info:
            javob_matni += f"🔹 1 **{info['Ccy']}** = {info['Rate']} so'm ({info['CcyNm_UZ']})\n"
            sana = info['Date'] # Sanani saqlab turamiz
        else:
            javob_matni += f"❌ {kod} kursini olib bo'lmadi.\n"

    javob_matni += f"\n📅 *Sana:* {sana}"
    
    # Natijani foydalanuvchiga yuborish (Markdown formatida)
    bot.send_message(message.chat.id, javob_matni, parse_mode='Markdown')

# Botni uzluksiz ishlatish
print("Bot ishga tushdi...")
bot.infinity_polling()
