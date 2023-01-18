import os
import sqlite3
from sqlite3 import Error
from settings import Paths


class DataBase:
    def __init__(self, path):
        self.path = path
        self.connection = None

    def create_connections(self):
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            print("Подключение к бд установлено!")
        except Error as e:
            print(f'Произошла ошибка {e} при подключении к базе данных')

    def execute_query(self, query, data_tuple=()):

        try:
            if data_tuple:
                self.cursor.execute(query, data_tuple)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Успешный запрос к бд")
        except Error as e:
            print(f"При запросе {query} произошла ошибка {e}")

    def create_table_vibropres(self):
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

    def convert_to_binary_data(self, file, path):
        """ Функция для конвертации файла в бинарный вид
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

    def get_file(self):
        get_file = """
        SELECT form, collection, color, photo
        FROM vibropres
        WHERE color = 'Базальт';"""
        self.execute_query(get_file)
        result = self.cursor.fetchall()
        return result[0][3]

    def close_connection(self):
        self.cursor.close()

if __name__ == "__main__":
    data = DataBase(Paths.path_to_database)

    data.create_connections()

#data.create_table_vibropres()
#data.add_to_table_vibropres(Paths.path_to_vibors)



