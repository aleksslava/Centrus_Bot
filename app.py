from telebot import TeleBot
from telebot.types import InputMediaPhoto
import db
from settings import token
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from db import DataBase
from settings import Paths


bot = TeleBot(token)

@bot.message_handler(commands=['start',])
def start(m):
    hello = 'Добро пожаловать в чат-бот компании Центрус.\nДля просмотра каталога нажмите на кнопку "Каталог".'
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    main_keyboard.row('Каталог')
    bot.send_message(m.chat.id, hello, reply_markup=main_keyboard)

@bot.message_handler(commands=['help',])
def help(m):
    help_message = """Для просмотра каталога нажмите кнопку "Каталог."""
    bot.send_message(m.chat.id, help_message)
@bot.message_handler(func=lambda message: message.text == 'Каталог')
def answer(m):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Тротуарная плитка", callback_data="bruschatka"))
    markup.add(InlineKeyboardButton(text="Облицовочная плитка", callback_data="fasade"))
    markup.add(InlineKeyboardButton(text="Системы водоотведения", callback_data="Water"))
    bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
    bot.send_message(m.chat.id, text="Выберите нужную категорию!", reply_markup=markup)

@bot.callback_query_handler(func=lambda m: m.data == "bruschatka")
def callback_bruschatka(m):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Вибропрессованная плитка", callback_data="vibropres"))
    markup.add(InlineKeyboardButton(text="Тротуарный клинкер", callback_data="klinker_trot"))
    bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    bot.send_message(m.message.chat.id, text="Выберите тип тротуарной плитки!", reply_markup=markup)

@bot.callback_query_handler(func=lambda m: m.data == "vibropres")
def vibropres(m):
    """Пока что не работает."""
    photos = db.DataBase(Paths.path_to_database)
    photos.create_connections()
    photos = photos.get_file()[:6]
    photos = list(map(InputMediaPhoto, photos))
    count = len(photos) // 5
    bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"1 из {count}", callback_data='_'),
               InlineKeyboardButton(text="Следующая", callback_data='next_vibor_2'))
    bot.send_message(m.message.chat.id, text='привет', reply_markup=markup)




bot.infinity_polling()