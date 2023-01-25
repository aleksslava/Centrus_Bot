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
    help_message = """Для просмотра фото образцов нажмите кнопку "Каталог."""
    bot.send_message(m.chat.id, help_message)
@bot.message_handler(func=lambda message: message.text == 'Каталог')
def answer(m):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Тротуарная плитка", callback_data="bruschatka"))
    markup.add(InlineKeyboardButton(text="Облицовочная плитка", callback_data="fasade"))
    markup.add(InlineKeyboardButton(text="Кирпич облицовочный", callback_data="next_kirpich_0"))
    markup.add(InlineKeyboardButton(text="Клинкерные ступени", callback_data="next_peldano_0"))
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

@bot.callback_query_handler(func=lambda m: (m.data.split('_')[1] == 'beton') if len(m.data.split('_')) > 1 else False)
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

@bot.callback_query_handler(func=lambda m: (m.data.split('_')[1] == 'klinker1') if len(m.data.split('_')) > 1 else False)
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

@bot.callback_query_handler(lambda m: m.data == 'fasade')
def callback_fasade1(m):
    bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Искусственный камень', callback_data='next_fkamen_0'))
    markup.add(InlineKeyboardButton(text='Декоративный кирпич', callback_data='next_fkirpich_0'))
    markup.add(InlineKeyboardButton(text='Клинкерная плитка', callback_data='next_fklinker_0'))
    bot.send_message(m.message.chat.id, text='Выберите категорию!', reply_markup=markup)

@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'fkamen') if len(m.data.split('_')) > 1 else False)
def callback_fasade_kamen_paginator(m):
    direction, _, count = m.data.split('_')
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    count_in_table = data.get_count_fasade('"искусственный_камень"')
    max_count = (count_in_table // 5) if count_in_table % 5 == 0 else (count_in_table // 5 + 1)
    photo_lst = data.get_file_from_fasade_kamen()
    markup = InlineKeyboardMarkup()
    if direction == 'next':
        count = int(count) + 1
        if count == max_count:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkamen_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkamen_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkamen_{count}')
            markup.add(button_1, button_2, button_3)
    else:
        count = int(count) - 1
        if count == 1:
            button_1 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_2 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkamen_{count}')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkamen_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkamen_{count}')
            markup.add(button_1, button_2, button_3)
    photo_lst= data.convert_to_output_fasade(count, photo_lst)
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'fkirpich') if len(m.data.split('_')) > 1 else False)
def callback_fasade_kirpich_paginator(m):
    direction, _, count = m.data.split('_')
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    count_in_table = data.get_count_fasade('"декоративный_кирпич"')
    max_count = (count_in_table // 5) if count_in_table % 5 == 0 else (count_in_table // 5 + 1)
    photo_lst = data.get_file_from_fasade_kirpich()
    markup = InlineKeyboardMarkup()
    if direction == 'next':
        count = int(count) + 1
        if count == max_count:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkirpich_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkirpich_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkirpich_{count}')
            markup.add(button_1, button_2, button_3)
    else:
        count = int(count) - 1
        if count == 1:
            button_1 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_2 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkirpich_{count}')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkirpich_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkirpich_{count}')
            markup.add(button_1, button_2, button_3)
    photo_lst = data.convert_to_output_fasade(count, photo_lst)
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)


@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'kirpich') if len(m.data.split('_')) > 1 else False)
def callback_kirpich_paginator(m):
    direction, _, count = m.data.split('_')
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    count_in_table = data.get_count_kirpich()
    max_count = (count_in_table // 5) if count_in_table % 5 == 0 else (count_in_table // 5 + 1)
    photo_lst = data.get_file_from_kirpich()
    markup = InlineKeyboardMarkup()
    if direction == 'next':
        count = int(count) + 1
        if count == max_count:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_kirpich_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_kirpich_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_kirpich_{count}')
            markup.add(button_1, button_2, button_3)
    else:
        count = int(count) - 1
        if count == 1:
            button_1 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_2 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_kirpich_{count}')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_kirpich_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_kirpich_{count}')
            markup.add(button_1, button_2, button_3)
    photo_lst = data.convert_to_output_kirpich(count, photo_lst)
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)


@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'peldano') if len(m.data.split('_')) > 1 else False)
def callback_peldano_paginator(m):
    direction, _, count = m.data.split('_')
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    count_in_table = data.get_count_peldano()
    max_count = (count_in_table // 5) if count_in_table % 5 == 0 else (count_in_table // 5 + 1)
    photo_lst = data.get_file_from_peldano()
    markup = InlineKeyboardMarkup()
    if direction == 'next':
        count = int(count) + 1
        if count == max_count:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_peldano_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_peldano_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_peldano_{count}')
            markup.add(button_1, button_2, button_3)
    else:
        count = int(count) - 1
        if count == 1:
            button_1 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_2 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_peldano_{count}')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_peldano_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_peldano_{count}')
            markup.add(button_1, button_2, button_3)
    photo_lst = data.convert_to_output_peldano(count, photo_lst)
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'fklinker') if len(m.data.split('_')) > 1 else False)
def callback_fklinker_paginator(m):
    direction, _, count = m.data.split('_')
    data = DataBase(Paths.path_to_database)
    data.create_connections()
    count_in_table = data.get_count_klinker()
    max_count = (count_in_table // 5) if count_in_table % 5 == 0 else (count_in_table // 5 + 1)
    photo_lst = data.get_file_from_fasade_klinker()
    markup = InlineKeyboardMarkup()
    if direction == 'next':
        count = int(count) + 1
        if count == max_count:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fklinker_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fklinker_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fklinker_{count}')
            markup.add(button_1, button_2, button_3)
    else:
        count = int(count) - 1
        if count == 1:
            button_1 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_2 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fklinker_{count}')
            markup.add(button_1, button_2)
        else:
            button_1 = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fklinker_{count}')
            button_2 = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
            button_3 = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fklinker_{count}')
            markup.add(button_1, button_2, button_3)
    photo_lst = data.convert_to_output_klinker(count, photo_lst)
    bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

"""
1) Сжать фото до меньших размеров.
2) Исправить пагинаторы.(пограничные значения не верно обрабатываются)
3) Создать функцию для поиска значений ограничения вывода фото и заменить код в функциях упаковки фото."""

bot.infinity_polling()