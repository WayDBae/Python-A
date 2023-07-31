import telebot
from telebot import types
import json
import requests
from datetime import datetime

TOKENTG = "6239532031:AAFq_oaH2k-inga8L3pIGws6woRvC9f9yVs"
ADMIN_CHAT_ID = 5417596910

bot = telebot.TeleBot(TOKENTG)

@bot.message_handler(commands=['start'])
def start(message):
    with open("users.json", "r") as f_o:
        data_from_json = json.load(f_o)
    user_id = message.from_user.id
    username = message.from_user.username
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username}
    with open("users.json", "w") as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii = False)
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lang = types.KeyboardButton("🇬🇧Language🇷🇺")
    key.add(lang)
    text = f"You're registered: {username}!\nYour user_id: {user_id}\nHello, {message.from_user.first_name}!\nWelcome to the bot."
    bot.send_message(message.chat.id, text,reply_markup=key)

def handle_standup_speech(message):
    bot.reply_to(message,"Спасибо большое! Желаем успехов и хорошего дня!")

@bot.message_handler(commands=['say_standup_speech'])
def say_standup_speech(message):
    bot.send_message(message.chat.id, "Привет! Чем ты занимался вчера?\nЧто будешь делать сегодня?\nКакие есть трудности?")
    bot.register_next_step_handler(message, handle_standup_speech)

@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    if message.text == "🇬🇧Language🇷🇺":
        key = types.InlineKeyboardMarkup()
        eng = types.InlineKeyboardButton("🇬🇧English🇬🇧", callback_data="en")
        rus = types.InlineKeyboardButton("🇷🇺Русский🇷🇺", callback_data="ru")
        key.add(eng,rus)
        bot.send_message(message.chat.id, "Choose language", reply_markup=key)

@bot.callback_query_handler(func=lambda call:True)
def all_calls(call):
    if call.data == "ru":
        saved = "Изменения сохранены."
        key = types.InlineKeyboardMarkup()
        schedule = types.InlineKeyboardButton("Расписание", callback_data="schedule")
        key.add(schedule)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = saved,reply_markup=key)
    elif call.data == "en":
        saved = "Changes saved."
        key = types.InlineKeyboardMarkup()
        schedule = types.InlineKeyboardButton("Schedule", callback_data="schedule")
        key.add(schedule)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = saved,reply_markup=key)
    elif call.data == "schedule":
        with open("tables.json", "r") as f_o:
            data = json.load(f_o)
        with open("tables.json", "w") as f_o:
            json.dump(data, f_o, indent=4, ensure_ascii = False)
            group_b_schedule = data.get("IT-RUN")  # Извлекаем расписание для моих групп
            nowaday = datetime.now().strftime('%A')
            for day, value in group_b_schedule.items():
                if day == nowaday:
                    todayschedule = f"Расписание на {day}:\n{value}"
                    bot.send_message(call.message.chat.id, todayschedule)

while True:
    try:
        bot.polling()
    except Exception as err:
        requests.post(f"https://api.telegram.org/bot{TOKENTG}/sendMessage?chat_id={ADMIN_CHAT_ID}&text=Время: {datetime.now()}\nТип ошибки: {err.__class__}\nОшибка: {err}")
