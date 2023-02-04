from peewee import *
from settings import Paths


db = SqliteDatabase(Paths.path_to_database)


class BaseModel(Model):
    class Meta:
        database = db

class Category(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)

    class Meta:
        db_table = "categories"

class Products(BaseModel):
    id = PrimaryKeyField(null=False)
    factory = CharField(max_length=100, null=False)
    form = CharField(max_length=100)
    collection = CharField(max_length=100, null=True)
    color = CharField(max_length=100, null=False)
    photo = BlobField(null=False)
    category = ForeignKeyField(Category, related_name='products')

    class Meta:
        db_table = 'products'



if __name__ == "__main__":
    pass
