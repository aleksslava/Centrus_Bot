from telebot.apihelper import ApiTelegramException
from settings import token
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from db1 import Data
from models import User
from telebot.async_telebot import AsyncTeleBot


bot = AsyncTeleBot(token)

@bot.message_handler(commands=['start',])
async def start(m):

    """Обработчик команды 'start', отправляет в чат reply кнопку 'Каталог'"""
    user, admin = Data.add_user(m.from_user, m.chat.id)
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if admin:
        hello = f"Добро пожаловать администратор {user}!\nВыберите в каком режиме вы хотите войти."
        main_keyboard.row('Панель_администратора')
    else:
        hello = f'{user}, добро пожаловать в чат-бот компании Центрус.\nДля просмотра каталога нажмите на кнопку "Каталог".'
    main_keyboard.row('Каталог')
    await bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
    await bot.send_message(m.chat.id, hello, reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text == "Панель_администратора")
async def panel_admin(m):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Получить список пользователей", callback_data='users'))
    user, admin = Data.add_user(m.from_user, m.chat.id)
    await bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
    if admin:
        await bot.send_message(m.chat.id, text="Выберите команду", reply_markup=keyboard)
    else:
        await bot.send_message(m.chat.id, text="У вас нет прав админа")

@bot.message_handler(commands=['help',])
async def help(m):
    """Обработчик команды 'help', отправляет в чат информацию о боте"""
    help_message = """Для просмотра фото образцов нажмите кнопку "Каталог."""
    await bot.send_message(m.chat.id, help_message)
@bot.message_handler(func=lambda message: message.text == 'Каталог')
async def catalog(m):
    """Обработчик кнопки "Каталог", отправляет в чат inline меню."""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Тротуарная плитка", callback_data="bruschatka"))
    markup.add(InlineKeyboardButton(text="Облицовочная плитка", callback_data="fasade"))
    markup.add(InlineKeyboardButton(text="Кирпич облицовочный", callback_data="next_kirpich_0"))
    markup.add(InlineKeyboardButton(text="Клинкерные ступени", callback_data="next_peldano_0"))
    await bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
    await bot.send_message(m.chat.id, text="Выберите нужную категорию!", reply_markup=markup)

@bot.callback_query_handler(func=lambda m: m.data == 'users')
async def callback_users_list(m):
    """Отправляет список клиентов в чат"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Сделать рассылку по клиентам", callback_data='spam'))
    users_list = Data.get_all_users()
    await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    await bot.send_message(m.message.chat.id, text=users_list, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda m: m.data == "spam")
async def spam(m):
    """обработчик рассылки по клиентам"""
    text = "Введите Ваше сообщение. Если передумали, то введите 'Отмена'"
    message = bot.send_message(m.message.chat.id, text=text)
    await bot.register_next_step_handler(message, spam_users)

async def spam_users(m):
    """Рассылка по клиентам принятого сообщения"""
    text = m.text
    if text == "Отмена":
        start(m)
    else:
        users = Data.get_users_for_send()
        for user in users:
            await bot.send_message(user.chat, text=text)
        await bot.send_message(m.message.chat.id, text="Готово!")

@bot.callback_query_handler(func=lambda m: m.data == "bruschatka")
async def callback_bruschatka(m):
    """Обработчик кнопки "Тротуарная плитка", отправляет в чат inline меню"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Вибропрессованная плитка", callback_data="next_beton_0"))
    markup.add(InlineKeyboardButton(text="Тротуарный клинкер", callback_data="next_klinker1_0"))
    await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    await bot.send_message(m.message.chat.id, text="Выберите тип тротуарной плитки!", reply_markup=markup)

@bot.callback_query_handler(lambda m: m.data == 'fasade')
async def callback_fasade1(m):
    """Обработчик кнопки "Фасадная плитка", отправляет в чат inline меню"""
    await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Искусственный камень', callback_data='next_fkamen_0'))
    markup.add(InlineKeyboardButton(text='Декоративный кирпич', callback_data='next_fkirpich_0'))
    markup.add(InlineKeyboardButton(text='Клинкерная плитка', callback_data='next_fklinker_0'))
    await bot.send_message(m.message.chat.id, text='Выберите категорию!', reply_markup=markup)


@bot.callback_query_handler(func=lambda m: (m.data.split('_')[1] == 'beton') if len(m.data.split('_')) > 1 else False)
async def callback_beton_pagination(m):
    """Обработчик кнопки "Вибропрессованная плитка", отправляет в чат фото-коллаж и кнопки навигации"""
    direction, table, count = m.data.split('_')
    max_count = Data.get_max_count(Data.category_list[table])
    markup = InlineKeyboardMarkup()
    count = int(count) + 1 if direction == "next" else int(count) - 1
    button_back = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_beton_{count}')
    button_middle = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
    button_next = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_beton_{count}')
    if count == 1:
        markup.add(button_middle, button_next)
    elif count == max_count:
        markup.add(button_back, button_middle)
    else:
        markup.add(button_back, button_middle, button_next)
    markup.add(InlineKeyboardButton(text="Запросить звонок менеджера.", callback_data='callphone'))
    photo_lst = Data.get_list_photo(count, Data.category_list[table])
    photo_lst = Data.convert_to_output(photo_lst)
    await bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    await bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda m: (m.data.split('_')[1] == 'klinker1') if len(m.data.split('_')) > 1 else False)
async def callback_feldhaus_trot_pagination(m):
    """Обработчик кнопки "Клинкерная плитка", отправляет в чат фото-коллаж и кнопки навигации"""
    direction, table, count = m.data.split('_')
    max_count = Data.get_max_count(Data.category_list[table])
    markup = InlineKeyboardMarkup()
    count = int(count) + 1 if direction == "next" else int(count) - 1
    button_back = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_klinker1_{count}')
    button_middle = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
    button_next = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_klinker1_{count}')
    if count == 1:
        markup.add(button_middle, button_next)
    elif count == max_count:
        markup.add(button_back, button_middle)
    else:
        markup.add(button_back, button_middle, button_next)
    markup.add(InlineKeyboardButton(text="Запросить звонок менеджера.", callback_data='callphone'))
    photo_lst = Data.get_list_photo(count, Data.category_list[table])
    photo_lst = Data.convert_to_output(photo_lst)
    await bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    await bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)


@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'fkamen') if len(m.data.split('_')) > 1 else False)
async def callback_fasade_kamen_paginator(m):
    """Обработчик кнопки "Искусственный камень", отправляет в чат фото-коллаж и кнопки навигации"""

    direction, table, count = m.data.split('_')
    max_count = Data.get_max_count(Data.category_list[table])
    markup = InlineKeyboardMarkup()
    count = int(count) + 1 if direction == "next" else int(count) - 1
    button_back = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkamen_{count}')
    button_middle = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
    button_next = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkamen_{count}')
    if count == 1:
        markup.add(button_middle, button_next)
    elif count == max_count:
        markup.add(button_back, button_middle)
    else:
        markup.add(button_back, button_middle, button_next)
    markup.add(InlineKeyboardButton(text="Запросить звонок менеджера.", callback_data='callphone'))
    photo_lst = Data.get_list_photo(count, Data.category_list[table])
    photo_lst = Data.convert_to_output(photo_lst)
    await bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    await bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'fkirpich') if len(m.data.split('_')) > 1 else False)
async def callback_fasade_kirpich_paginator(m):
    """Обработчик кнопки "Декоративный кирпич", отправляет в чат фото-коллаж и кнопки навигации"""
    direction, table, count = m.data.split('_')
    max_count = Data.get_max_count(Data.category_list[table])
    markup = InlineKeyboardMarkup()
    count = int(count) + 1 if direction == "next" else int(count) - 1
    button_back = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fkirpich_{count}')
    button_middle = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
    button_next = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fkirpich_{count}')
    if count == 1:
        markup.add(button_middle, button_next)
    elif count == max_count:
        markup.add(button_back, button_middle)
    else:
        markup.add(button_back, button_middle, button_next)
    markup.add(InlineKeyboardButton(text="Запросить звонок менеджера.", callback_data='callphone'))
    photo_lst = Data.get_list_photo(count, Data.category_list[table])
    photo_lst = Data.convert_to_output(photo_lst)
    await bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    await bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)


@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'kirpich') if len(m.data.split('_')) > 1 else False)
async def callback_kirpich_paginator(m):
    """Обработчик кнопки "Облицовочный кирпич", отправляет в чат фото-коллаж и кнопки навигации"""
    direction, table, count = m.data.split('_')
    max_count = Data.get_max_count(Data.category_list[table])
    markup = InlineKeyboardMarkup()
    count = int(count) + 1 if direction == "next" else int(count) - 1
    button_back = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_kirpich_{count}')
    button_middle = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
    button_next = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_kirpich_{count}')
    if count == 1:
        markup.add(button_middle, button_next)
    elif count == max_count:
        markup.add(button_back, button_middle)
    else:
        markup.add(button_back, button_middle, button_next)
    markup.add(InlineKeyboardButton(text="Запросить звонок менеджера.", callback_data='callphone'))
    photo_lst = Data.get_list_photo(count, Data.category_list[table])
    photo_lst = Data.convert_to_output(photo_lst)
    await bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    await bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)


@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'peldano') if len(m.data.split('_')) > 1 else False)
async def callback_peldano_paginator(m):
    """Обработчик кнопки "Клинкерные ступени", отправляет в чат фото-коллаж и кнопки навигации"""
    direction, table, count = m.data.split('_')
    max_count = Data.get_max_count(Data.category_list[table])
    markup = InlineKeyboardMarkup()
    count = int(count) + 1 if direction == "next" else int(count) - 1
    button_back = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_peldano_{count}')
    button_middle = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
    button_next = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_peldano_{count}')
    if count == 1:
        markup.add(button_middle, button_next)
    elif count == max_count:
        markup.add(button_back, button_middle)
    else:
        markup.add(button_back, button_middle, button_next)
    markup.add(InlineKeyboardButton(text="Запросить звонок менеджера.", callback_data='callphone'))
    photo_lst = Data.get_list_photo(count, Data.category_list[table])
    photo_lst = Data.convert_to_output(photo_lst)
    await bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    await bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

@bot.callback_query_handler(lambda m: (m.data.split('_')[1] == 'fklinker') if len(m.data.split('_')) > 1 else False)
async def callback_fklinker_paginator(m):
    """Обработчик кнопки "Клинкерная плитка", отправляет в чат фото-коллаж и кнопки навигации"""
    direction, table, count = m.data.split('_')
    max_count = Data.get_max_count(Data.category_list[table])
    markup = InlineKeyboardMarkup()
    count = int(count) + 1 if direction == "next" else int(count) - 1
    button_back = InlineKeyboardButton(text=f'<---Назад', callback_data=f'back_fklinker_{count}')
    button_middle = InlineKeyboardButton(text=f'{count} из {max_count}', callback_data='_')
    button_next = InlineKeyboardButton(text='Вперед--->', callback_data=f'next_fklinker_{count}')
    if count == 1:
        markup.add(button_middle, button_next)
    elif count == max_count:
        markup.add(button_back, button_middle)
    else:
        markup.add(button_back, button_middle, button_next)
    markup.add(InlineKeyboardButton(text="Запросить звонок менеджера.", callback_data='callphone'))
    photo_lst = Data.get_list_photo(count, Data.category_list[table])
    photo_lst = Data.convert_to_output(photo_lst)
    await bot.send_media_group(m.message.chat.id, photo_lst)
    try:
        await bot.delete_message(chat_id=m.message.chat.id, message_id=m.message.message_id)
    except ApiTelegramException as e:
        print(f'Удалить сообщение не удалось! Ошибка {e}')
    await bot.send_message(m.message.chat.id, text='Для просмотра названия формы и цвета нажмите на фото!',
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda m: m.data == 'callphone')
async def get_phone(m):
    text = "Отправить телефон!"
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text=text, request_contact=True))
    await bot.send_message(m.message.chat.id, text="Нажмите на кнопку", reply_markup=keyboard)

@bot.message_handler(content_types=['contact',])
async def contact(m):
    await bot.delete_message(m.chat.id, m.id)
    await bot.send_message(m.chat.id, text="В ближайшее время с Вами свяжется менеджер.")
    phone = m.contact.phone_number
    user_id = m.from_user.id
    Data.add_phone_number(user_id, phone)
    admins = Data.get_admins()
    user = User.get(User.user_id == user_id)
    keyboard = ReplyKeyboardRemove()
    for admin in admins:
        await bot.send_message(admin.chat, text=f"Запрос звонка от клиента: {user.first_name} {user.last_name}, Ник: {user.username},"
                                          f" телефон: {user.telephone}", reply_markup=keyboard)

import asyncio
asyncio.run(bot.polling())