import os.path
import pathlib

# token = "5873053286:AAGFQvZm2o1pHSWlHQ2Q_IJ8F_l1jXfJDTM"
with open('TOKEN.txt', 'r') as file:
    token = file.read().replace('\r\n', '')


class Paths:
    path_to_database = pathlib.Path('database').absolute().__str__() + r'\data_items.sqlite'
    path_to_vibors = r'D:\Python_code\Centrus_Bot\vibors_photo'
    path_to_feldhaus_trot = r'D:\Python_code\Centrus_Bot\feldhaus_trot'
    path_to_kamelot = r'D:\Python_code\Centrus_Bot\fasade'
    path_to_portland = r'D:\Python_code\Centrus_Bot\fasade2'
    path_to_kirpich = r'D:\Python_code\Centrus_Bot\kirpich'
    path_to_peldano = r'D:\Python_code\Centrus_Bot\peldano'
    path_to_klinker = r'D:\Python_code\Centrus_Bot\klinker'