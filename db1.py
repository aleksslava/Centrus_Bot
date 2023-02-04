import os

from peewee import *
from settings import Paths
from models import Products
from models import Category
from telebot.types import InputMediaPhoto


class Data:

    category_list = {
        "beton": "тротуарная_плитка",
        "klinker1": "тротуарный_клинкер",
        "kirpich": "облицовочный_кирпич",
        "peldano": "ступени",
        "fkamen": "искусственный_камень",
        "fkirpich": "декоративный_кирпич",
        "fklinker": "фасадный_клинкер"
    }

    capture_list = {
        "factory": "Завод",
        "form": "Форма",
        "collection": "Коллекция",
        "color": "Цвет",
        "photo": "фото"
    }

    @staticmethod
    def convert_to_binary_data(file, path):
        """ Функция для конвертации фото в бинарный вид
        """
        with open(path.joinpath(file), 'rb') as photo:
            blob_file = photo.read()
            return blob_file

    @staticmethod
    def add_to_products(path):
        list_of_items = os.listdir(path)

        for item in list_of_items:
            title, _ = item.split('.')
            factory, color = title.split()
            form = 'кирпич'
            category = Category.get(Category.name == "облицовочный_кирпич")
            photo = Data.convert_to_binary_data(item, path)
            file = Products(factory=factory, form=form, color=color, photo=photo, category=category)
            file.save()
            print(f"{item}, успешно добавлен в таблицу")

    @staticmethod
    def get_max_count(category):
        """Функция возвращает количество элементов в таблице по выбранной категории."""
        count = Products.select().join(Category).where(Category.name == category).count()
        max_count = (count // 5) if count % 5 == 0 else (count // 5 + 1)
        return max_count

    @staticmethod
    def convert_to_output(lst):
        output = []
        for file in lst:
            capture = ''
            attr_list = {'factory': file.factory,
                            'form': file.form,
                            'collection': file.collection,
                            'color': file.color,
                            'photo': ''}
            for key, value in attr_list.items():
                if value:
                    capture += f'{Data.capture_list[key]}: {value}\n'
            output.append(InputMediaPhoto(media=file.photo, caption=capture))
        return output

    @staticmethod
    def get_list_photo(count, table):
        count = (count - 1) * 5
        lst = Products.select().join(Category).where(Category.name == table).offset(count).limit(5)
        return lst



if __name__ == "__main__":
    lst = Data.get_list_photo(1, Data.category_list['beton'])
    files = Data.convert_to_output(lst)
    for file in files:
        print(file.media)

