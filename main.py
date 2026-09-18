import telebot
import requests
import time

BOT_TOKEN = "8933278279:AAFMQLAn9ujXJyF9TxaRITdYwZiKX-iGC3U
BINDERBYTE_API = "sk_en99yadtsidveh8ha14oy3rddyxdsudfcjgw0gd5imokpx6kv9onnbu0snph61fb"

bot = telebot.TeleBot(BOT_TOKEN)
couriers = ["jne","jnt","sicepat","anteraja","wahana","ninja","lion","pos","spx","idexpress","tiki"]
user_courier = {}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🤖 BOT SULTAN SIAP!\nKetik kurir: jne/jnt/sicepat dll\nLalu kirim resi (bisa 100 resi sekaligus)")

@bot.message_handler(func=lambda m: m.text.lower().strip() in couriers)
def set_courier(m):
    user_courier[m.chat.id] = m.text.lower().strip()
    bot.send_message(m.chat.id, f"✅ Kurir {m.text.upper()} dipilih! Kirim resi nya:")

@bot.message_handler(func=lambda m: True)
def cek(m):
    awbs = [x for x in m.text.replace(","," ").split() if len(x)>8]
    if not awbs: return
    pref = user_courier.get(m.chat.id)
    clist = [pref]+couriers if pref else couriers
    for awb in awbs[:100]:
        for courier in clist:
            if not courier: continue
            try:
                url = f"https://api.binderbyte.com/v1/track?api_key={BINDERBYTE_API}&courier={courier}&awb={awb}"
                r = requests.get(url, timeout=15).json()
                if r.get("status")==200:
                    s = r['data']['summary']
                    bot.send_message(m.chat.id, f"✅ {courier.upper()} - {awb}\nStatus: {s['status']}\n{s['desc']}")
                    break
            except: continue

bot.infinity_polling()
