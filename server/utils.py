import datetime
import credentials
import shutil
from os import getcwd, mkdir
from os.path import join as pjoin

def nuke_users_dir(rootdir):
    upload_path = pjoin(getcwd(), 'uploads')
    shutil.rmtree(upload_path)
    mkdir(upload_path)


def current_timestamp():
    return datetime.datetime.now().strftime('%d%m%Y %H%M%S%f')
