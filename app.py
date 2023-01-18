from telebot import TeleBot
from settings import token
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
bot = TeleBot(token)
from db import DataBase
from settings import Paths

@bot.message_handler(commands=['start',])
def start(m):
    hello = 'Добро пожаловать в чат-бот компании центрус.\nВы можете воспользоваться меню.'
    main_keyboard = ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True, one_time_keyboard=True)
    main_keyboard.row('Тротуарная плитка', 'Фасадная плитка')
    main_keyboard.row('Системы водоотведения', 'Системы грязезащиты')

    bot.send_message(m.chat.id, hello, reply_markup=main_keyboard)

@bot.message_handler(commands=['help',])
def help(m):
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    file = data.get_file()
    bot.send_photo(m.chat.id, photo=file, caption="Выбор-с Базальт Антара")

@bot.message_handler(content_types=['text'])
def answer(m):
    if m.text == 'Тротуарная плитка':
        keyboard = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Вибропрессованная плитка", callback_data='beton')
        button_2 = InlineKeyboardButton(text="Клинкерная плитка", callback_data='clinker')
        keyboard.add(button_1, button_2)
        bot.send_message(m.chat.id, 'Виды тротуарной плитки', reply_markup=keyboard)
    elif m.text == 'Фасадная плитка':
        keyboard = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton("Декоративный камень", callback_data='beton_phasade')
        button_2 = InlineKeyboardButton("Клинкерная плитка", callback_data='clinker_phasade')
        keyboard.add(button_1, button_2)
        bot.send_message(m.chat.id, 'Виды тротуарной плитки', reply_markup=keyboard)
    elif m.text == 'Системы водоотведения':
        pass
    elif m.text == 'Системы грязезащиты':
        pass



bot.polling(non_stop=True)