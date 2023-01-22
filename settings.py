import pathlib

# token = "5873053286:AAGFQvZm2o1pHSWlHQ2Q_IJ8F_l1jXfJDTM"
with open('TOKEN.txt', 'r') as file:
    token = file.read().replace('\r\n', '')


class Paths:
    path_to_database = pathlib.Path('database').absolute().__str__() + r'\data_items.sqlite'
    path_to_vibors = r'D:\Python_code\Centrus_Bot\vibors_photo'
    path_to_feldhaus_trot = r'D:\Python_code\Centrus_Bot\feldhaus_trot'