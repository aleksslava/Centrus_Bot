import os.path
import pathlib
from pathlib import Path

# token = "5873053286:AAGFQvZm2o1pHSWlHQ2Q_IJ8F_l1jXfJDTM"
with open('TOKEN.txt', 'r') as file:
    token = file.read().replace('\r\n', '')


class Paths:
    path_to_database = Path('database\data_items.sqlite')
    path_to_vibors = Path('vibors_photo')
    path_to_feldhaus_trot = Path('feldhaus_trot')
    path_to_kamelot = Path('fasade')
    path_to_portland = Path('fasade2')
    path_to_kirpich = Path('kirpich')
    path_to_peldano = Path('peldano')
    path_to_klinker = Path('klinker')

