from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from settings import token
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from db import DataBase
from settings import Paths
import time


bot = TeleBot(token)

@bot.message_handler(commands=['start',])
def start(m):
    """Обработчик команды 'start', отправляет в чат reply кнопку 'Каталог'"""
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

    data = DataBase(Paths.path_to_database)
    data.create_connections()
    photo_lst = data.get_file_from_vibropres()
    count = 1
    photo_lst, max_count  = data.convert_to_output_vibropres(1, photo_lst)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"1 из {max_count}", callback_data='_'),
               InlineKeyboardButton(text="Вперед--->", callback_data=f'next_beton_{count}_{max_count}'))
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!', reply_markup=markup)

@bot.callback_query_handler(func=lambda m: m.data.split('_')[1] == 'beton')
def beton_pagination(m):
    direction, _, count, max_count = m.data.split('_')
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    photo_lst = data.get_file_from_vibropres()
    markup = InlineKeyboardMarkup()
    if direction == 'next':
        count = int(count) + 1
        if count == max_count:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_beton_{count}_{max_count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_beton_{count}_{max_count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_beton_{count}_{max_count}')
            markup.add(button_1, button_2, button_3)
    else:
        count = int(count) - 1
        if count == 1:
            button_1 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_2 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_beton_{count}_{max_count}')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_beton_{count}_{max_count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_beton_{count}_{max_count}')
            markup.add(button_1, button_2, button_3)
    photo_lst, max_count = data.convert_to_output_vibropres(count, photo_lst)
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda m: m.data == "klinker_trot")
def callback_klinker(m):
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    photo_lst = data.get_file_from_klinker_trot()
    count = 1
    photo_lst, max_count = data.convert_to_output_feldhaus_trot(1, photo_lst)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"1 из {max_count}", callback_data='_'),
               InlineKeyboardButton(text="Вперед--->", callback_data=f'next_klinker1_{count}_{max_count}'))
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda m: m.data.split('_')[1] == 'klinker1')
def feldhaus_trot_pagination(m):
    direction, _, count, max_count = m.data.split('_')
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    photo_lst = data.get_file_from_klinker_trot()
    markup = InlineKeyboardMarkup()
    if direction == 'next':
        count = int(count) + 1
        if count == max_count:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_klinker1_{count}_{max_count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_klinker1_{count}_{max_count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_klinker1_{count}_{max_count}')
            markup.add(button_1, button_2, button_3)
    else:
        count = int(count) - 1
        if count == 1:
            button_1 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_2 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_klinker1_{count}_{max_count}')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_klinker1_{count}_{max_count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_klinker1_{count}_{max_count}')
            markup.add(button_1, button_2, button_3)
    photo_lst, max_count = data.convert_to_output_feldhaus_trot(count, photo_lst)
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)


bot.infinity_polling()