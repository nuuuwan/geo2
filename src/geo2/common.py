import os

DIR_DATA = '/tmp/geo2.data'


def init_dir_data():
    if not os.path.exists(DIR_DATA):
        os.mkdir(DIR_DATA)
