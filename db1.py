import os
from models import Products, User
from models import Category
from telebot.types import InputMediaPhoto
from peewee import IntegrityError
import json

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

    @staticmethod
    def add_user(user, chat):
        first_name = user.first_name
        last_name = user.last_name
        id = user.id
        admin = False
        username = user.username
        try:
            user = User(first_name=first_name, last_name=last_name, user_id=id, admin=admin, chat=chat, username=username)
            user.save()
        except IntegrityError:
            pass
        output = User.select().where(User.user_id == id)
        return output[0].first_name, output[0].admin
    @staticmethod
    def get_all_users():
        lst = User.select()
        output = ''
        for user in lst:
            user = dict(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                phone=user.telephone
            )
            user = json.dumps(user, ensure_ascii=False)
            output += user + '\n'
        return output
    @staticmethod
    def get_users_for_send():
        return User.select()

    @staticmethod
    def add_phone_number(user_id, phone_number):
        user = User.get(User.user_id == user_id)
        user.telephone = phone_number
        user.save()

    @staticmethod
    def get_admins():
        admins = User.select().where(User.admin == True)
        return admins

if __name__ == "__main__":
    print(Data.get_all_users())



