import os
import sqlite3
from sqlite3 import Error
from settings import Paths
from telebot.types import InputMediaPhoto




class DataBase:
    """Класс для взаимодействия с базой данных SQL"""
    def __init__(self, path):
        self.path = path
        self.connection = None
    @staticmethod
    def slice(num, max_count, len_lst):
        """Функция для расчета среза, для выдачи из бд.
        На вход принимает текущую страницу, общее количество страниц, количество элементов в списке
        """
        if num == 1:
            start = 0
            end = 5
        elif 1 < num < max_count:
            start = (num - 1) * 5
            end = num * 5
        else:
            start = (num - 1) * 5
            end = len_lst
        return start, end
    def create_connections(self):
        """Функция осуществляет соединение с бд"""
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f'Произошла ошибка {e} при подключении к базе данных')

    def execute_query(self, query, data_tuple=()):
        """Функция для отправки запроса в бд"""

        try:
            if data_tuple:
                self.cursor.execute(query, data_tuple)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"При запросе {query} произошла ошибка {e}")

    def create_table_vibropres(self):
        """Функция для создании таблицы vibropres"""
        vibropres_table = """
        CREATE TABLE IF NOT EXISTS vibropres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factory TEXT NOT NULL,
        form TEXT NOT NULL,
        collection TEXT NOT NULL,
        color TEXT NOT NULL,
        photo BLOB NOT NULL);
        """
        self.execute_query(vibropres_table)

    def create_table_clinker_trot(self):
        """Функция для создании таблицы clinker_trot"""
        clinker_trot = """
        CREATE TABLE IF NOT EXISTS clinker_trot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factory TEXT NOT NULL,
        form TEXT NOT NULL,
        color TEXT NOT NULL,
        photo BLOB NOT NULL);
        """
        self.execute_query(clinker_trot)

    def create_table_fasade(self):
        """Функция для создания таблицы fasade"""
        table_fasade = """
        CREATE TABLE IF NOT EXISTS fasade (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factory TEXT NOT NULL,
        form TEXT NOT NULL,
        collection TEXT NOT NULL,
        color TEXT NOT NULL,
        photo BLOB NOT NULL);
        """
        self.execute_query(table_fasade)

    def create_table_klinker(self):
        """Функция для создании таблицы klinker"""
        table_klinker = """
        CREATE TABLE IF NOT EXISTS klinker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factory TEXT NOT NULL,
        form TEXT NOT NULL,
        color TEXT NOT NULL,
        photo BLOB NOT NULL);
        """
        self.execute_query(table_klinker)

    def create_table_kirpich(self):
        """Функция для создании таблицы kirpich"""
        table_kirpich = """
        CREATE TABLE IF NOT EXISTS kirpich (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factory TEXT NOT NULL,
        color TEXT NOT NULL,
        photo BLOB NOT NULL);
        """
        self.execute_query(table_kirpich)

    def create_table_peldano(self):
        """Функция для создании таблицы peldano"""
        table_peldano = """
        CREATE TABLE IF NOT EXISTS peldano (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factory TEXT NOT NULL,
        collection TEXT NOT NULL,
        color TEXT NOT NULL,
        photo BLOB NOT NULL);
        """
        self.execute_query(table_peldano)

    def convert_to_binary_data(self, file, path):
        """ Функция для конвертации фото в бинарный вид
        """
        with open(path + '\\' + file, 'rb') as photo:
            blob_file = photo.read()
            return blob_file


    def add_to_table_vibropres(self, path):
        """ Функция для добавления записей в таблицу vibropres"""
        list_of_items = os.listdir(path)
        for file in list_of_items:

            title, _ = file.split('.')
            factory, form, collection, color = title.split()
            photo = self.convert_to_binary_data(file, path)
            data_tuple = (factory, form, collection, color, photo)
            pattern_query = f"""
            INSERT INTO vibropres (factory, form, collection, color, photo) 
            VALUES (?, ?, ?, ?, ?);"""
            try:
                self.execute_query(pattern_query, data_tuple)

                print(f'В базу данных успешно добавлен файл: "{file}"')
            except Exception as e:
                print(f'При добавлении {file} произошла ошибка {e}')
                continue

    def add_to_clinker_trot(self, path):
        """ Функция для добавления записей в таблицу clinker_trot"""
        list_of_items = os.listdir(path)
        for file in list_of_items:

            title, _ = file.split('.')
            factory, form, color = title.split()
            photo = self.convert_to_binary_data(file, path)
            data_tuple = (factory, form, color, photo)
            pattern_query = f"""
                    INSERT INTO clinker_trot (factory, form, color, photo) 
                    VALUES (?, ?, ?, ?);"""
            try:
                self.execute_query(pattern_query, data_tuple)

                print(f'В базу данных успешно добавлен файл: "{file}"')
            except Exception as e:
                print(f'При добавлении {file} произошла ошибка {e}')
                continue

    def add_to_table_fasade(self, path):
        """ Функция для добавления записей в таблицу fasade"""
        list_of_items = os.listdir(path)
        for file in list_of_items:

            title, _ = file.split('.')
            factory, form, collection, color = title.split()
            photo = self.convert_to_binary_data(file, path)
            data_tuple = (factory, form, collection, color, photo)
            pattern_query = f"""
                            INSERT INTO fasade (factory, form, collection, color, photo) 
                            VALUES (?, ?, ?, ?, ?);"""
            try:
                self.execute_query(pattern_query, data_tuple)

                print(f'В базу данных успешно добавлен файл: "{file}"')
            except Exception as e:
                print(f'При добавлении {file} произошла ошибка {e}')
                continue

    def add_to_table_klinker(self, path):
        """ Функция для добавления записей в таблицу klinker"""
        list_of_items = os.listdir(path)
        for file in list_of_items:

            title, _ = file.split('.')
            factory, form, color = title.split()
            photo = self.convert_to_binary_data(file, path)
            data_tuple = (factory, form, color, photo)
            pattern_query = f"""
                            INSERT INTO klinker (factory, form, color, photo) 
                            VALUES (?, ?, ?, ?);"""
            try:
                self.execute_query(pattern_query, data_tuple)

                print(f'В базу данных успешно добавлен файл: "{file}"')
            except Exception as e:
                print(f'При добавлении {file} произошла ошибка {e}')
                continue

    def add_to_table_kirpich(self, path):
        """ Функция для добавления записей в таблицу kirpich"""
        list_of_items = os.listdir(path)
        for file in list_of_items:

            title, _ = file.split('.')
            factory, color = title.split()
            photo = self.convert_to_binary_data(file, path)
            data_tuple = (factory, color, photo)
            pattern_query = f"""
                                    INSERT INTO kirpich (factory, color, photo) 
                                    VALUES (?, ?, ?);"""
            try:
                self.execute_query(pattern_query, data_tuple)

                print(f'В базу данных успешно добавлен файл: "{file}"')
            except Exception as e:
                print(f'При добавлении {file} произошла ошибка {e}')
                continue

    def add_to_table_peldano(self, path):
        """ Функция для добавления записей в таблицу peldano"""
        list_of_items = os.listdir(path)
        for file in list_of_items:

            title, _ = file.split('.')
            factory, collection, color = title.split()
            photo = self.convert_to_binary_data(file, path)
            data_tuple = (factory, collection, color, photo)
            pattern_query = f"""
                                            INSERT INTO peldano (factory, collection, color, photo) 
                                            VALUES (?, ?, ?, ?);"""
            try:
                self.execute_query(pattern_query, data_tuple)

                print(f'В базу данных успешно добавлен файл: "{file}"')
            except Exception as e:
                print(f'При добавлении {file} произошла ошибка {e}')
                continue

    def get_file_from_vibropres(self):
        """ Функция для извлечения записей из таблицы vibropres"""
        get_file = """
        SELECT factory, form, collection, color, photo
        FROM vibropres
        ;"""
        self.execute_query(get_file)
        result = self.cursor.fetchall()
        return result

    def get_file_from_klinker_trot(self):
        """ Функция для извлечения записей из таблицы clinker_trot"""
        get_file = """
        SELECT factory, form, color, photo
        FROM clinker_trot
        ;"""
        self.execute_query(get_file)
        result = self.cursor.fetchall()
        return result
    def get_file_from_fasade_kirpich(self):
        """ Функция для извлечения записей из таблицы fasade"""
        query = """
        SELECT factory, form, collection, color, photo
        FROM fasade
        WHERE form = 'декоративный_кирпич'
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return result

    def get_file_from_fasade_kamen(self):
        """ Функция для извлечения записей из таблицы fasade"""
        query = """
        SELECT factory, form, collection, color, photo
        FROM fasade
        WHERE form = 'искусственный_камень'
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return result

    def get_file_from_fasade_klinker(self):
        """ Функция для извлечения записей из таблицы klinker"""
        query = """
        SELECT factory, form, color, photo
        FROM klinker
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return result

    def get_file_from_kirpich(self):
        """ Функция для извлечения записей из таблицы kirpich"""
        query = """
        SELECT factory, color, photo
        FROM kirpich
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return result

    def get_file_from_peldano(self):
        """ Функция для извлечения записей из таблицы peldano"""
        query = """
        SELECT factory, collection, color, photo
        FROM peldano
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return result

    def close_connection(self):
        """Функция для закрытия соединения с бд"""
        self.cursor.close()

    @staticmethod
    def convert_to_output_vibropres(num, lst):
        """Функция для упаковки фото в список"""

        len_lst = len(lst)
        flag = True if len_lst % 5 == 0 else False
        if flag:
            max_count = len_lst // 5
        else:
            max_count = len_lst // 5 + 1
        start, end = DataBase.slice(num, max_count, len_lst)

        result = []
        lst = lst[start:end]

        for row in lst:
            factory, form, collection, color, photo = row
            result.append(InputMediaPhoto(media=photo, caption=f"""Завод: {factory}\nФорма: {form}\nКоллекция: {collection}\nЦвет: {color}"""))
        return result

    @staticmethod
    def convert_to_output_feldhaus_trot(num, lst):
        """Функция для упаковки фото в список"""
        len_lst = len(lst)
        flag = True if len_lst % 5 == 0 else False
        if flag:
            max_count = len_lst // 5
        else:
            max_count = len_lst // 5 + 1
        start, end = DataBase.slice(num, max_count, len_lst)

        result = []
        lst = lst[start:end]
        for row in lst:
            factory, form, color, photo = row
            result.append(InputMediaPhoto(media=photo,
                                          caption=f"""Завод: {factory}\nФорма: {form}\nЦвет: {color}"""))
        return result

    @staticmethod
    def convert_to_output_fasade(num, lst):
        """Функция для упаковки фото в список"""
        len_lst = len(lst)
        flag = True if len_lst % 5 == 0 else False
        if flag:
            max_count = len_lst // 5
        else:
            max_count = len_lst // 5 + 1
        start, end = DataBase.slice(num, max_count, len_lst)

        result = []
        lst = lst[start:end]

        for row in lst:
            factory, form, collection, color, photo = row
            result.append(InputMediaPhoto(media=photo,
                                          caption=f"""Завод: {factory}\nФорма: {form}\nКоллекция: {collection}\nЦвет: {color}"""))
        return result

    @staticmethod
    def convert_to_output_kirpich(num, lst):
        """Функция для упаковки фото в список"""
        len_lst = len(lst)
        flag = True if len_lst % 5 == 0 else False
        if flag:
            max_count = len_lst // 5
        else:
            max_count = len_lst // 5 + 1
        start, end = DataBase.slice(num, max_count, len_lst)

        result = []
        lst = lst[start:end]

        for row in lst:
            factory, color, photo = row
            result.append(InputMediaPhoto(media=photo,
                                          caption=f"""Завод: {factory}\nЦвет: {color}"""))
        return result

    @staticmethod
    def convert_to_output_klinker(num, lst):
        """Функция для упаковки фото в список"""
        len_lst = len(lst)
        flag = True if len_lst % 5 == 0 else False
        if flag:
            max_count = len_lst // 5
        else:
            max_count = len_lst // 5 + 1
        start, end = DataBase.slice(num, max_count, len_lst)

        result = []
        lst = lst[start:end]

        for row in lst:
            factory, form, color, photo = row
            result.append(InputMediaPhoto(media=photo,
                                          caption=f"""Завод: {factory}\nФорма: {form}\nЦвет: {color}"""))
        return result


    @staticmethod
    def convert_to_output_peldano(num, lst):
        """Функция для упаковки фото в список"""
        len_lst = len(lst)
        flag = True if len_lst % 5 == 0 else False
        if flag:
            max_count = len_lst // 5
        else:
            max_count = len_lst // 5 + 1
        start, end = DataBase.slice(num, max_count, len_lst)

        result = []
        lst = lst[start:end]

        for row in lst:
            factory, collection, color, photo = row
            result.append(InputMediaPhoto(media=photo,
                                          caption=f"""Завод: {factory}\nКоллекция: {collection}\nЦвет: {color}"""))
        return result


    def get_count_fasade(self, form):
        """Функция возвращает количество строк в таблице fasade"""
        query = f"""
        SELECT COUNT(id)
        FROM fasade
        WHERE form = {form};"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return int(result[0][0])

    def get_count_kirpich(self):
        """Функция возвращает количество строк в таблице kirpich"""
        query = """
        SELECT COUNT(id)
        FROM kirpich
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return int(result[0][0])

    def get_count_peldano(self):
        """Функция возвращает количество строк в таблице peldano"""
        query = """
        SELECT COUNT(id)
        FROM peldano
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return int(result[0][0])

    def get_count_klinker(self):
        """Функция возвращает количество строк в таблице klinker"""
        query = """
        SELECT COUNT(id)
        FROM klinker
        ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return int(result[0][0])

    def get_count_vibropres(self):
        """Функция возвращает количество строк в таблице vibropres"""
        query = """
                SELECT COUNT(id)
                FROM vibropres
                ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return int(result[0][0])
    
    def get_count_klinker_trot(self):
        """Функция возвращает количество строк в таблице clinker_trot"""
        query = """
                SELECT COUNT(id)
                FROM clinker_trot
                ;"""
        self.execute_query(query)
        result = self.cursor.fetchall()
        return int(result[0][0])

if __name__ == "__main__":
    data = DataBase(Paths.path_to_database)
    data.create_connections()






