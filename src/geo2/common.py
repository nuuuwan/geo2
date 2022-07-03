import os
import shutil

DIR_DATA = '/tmp/geo2.data'


def init_dir_data():
    if os.path.exists(DIR_DATA):
        shutil.rmtree(DIR_DATA)
    os.mkdir(DIR_DATA)
