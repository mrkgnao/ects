import datetime
import credentials
import shutil
from os import getcwd, mkdir
from os.path import join as pjoin

def current_timestamp():
    return datetime.datetime.now().strftime('%d%m%Y %H%M%S%f')
