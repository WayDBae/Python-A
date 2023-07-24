import telebot
from telebot import types

API = "6308251077:AAGYufpx4jKSEt_Gmeko62L8j71Mttxk8n4"

bot = telebot.TeleBot(API)


@bot.message_handler(commands=['start'])
def start(message):
    # key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # python = types.KeyboardButton("Python")
    # cpp = types.KeyboardButton("C++")
    # key.add(python,cpp)
    key = types.InlineKeyboardMarkup()
    py = types.InlineKeyboardButton("Python",callback_data="py")
    cpp = types.InlineKeyboardButton("C++", callback_data="cpp")
    key.add(py,cpp)
    bot.send_message(message.chat.id, "Привет! Выбери язык программирования: ",reply_markup=key)

@bot.callback_query_handler(func = lambda call: True)
def handler(call):
    if call.data == "py":
        key = types.InlineKeyboardMarkup()
        mainpy = types.InlineKeyboardButton("Основы Python",callback_data="mainpy")
        tgbot = types.InlineKeyboardButton("Telegram Bots", callback_data="tgbot")
        key.add(mainpy,tgbot)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Выберите тему: ",reply_markup=key)
    elif call.data == "cpp":
        key = types.InlineKeyboardMarkup()
        maincpp = types.InlineKeyboardButton("Основы C++", callback_data="maincpp")
        qt = types.InlineKeyboardButton("Qt for C++", callback_data="qt")
        key.add(maincpp,qt)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Выберите тему: ",reply_markup=key)

bot.infinity_polling()