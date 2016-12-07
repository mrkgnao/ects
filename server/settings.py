import datetime
from os.path import join as pjoin

SERVER_URL           = "http://localhost:8080"
SERVER_UPLOAD_SUFFIX = pjoin("/upload", str(datetime.datetime.now().year))
SERVER_UPLOAD_URL    = SERVER_URL + SERVER_UPLOAD_SUFFIX

FILE_UPLOAD_FIELD_NAME = "upload_file"

NUKE_SAVED_FILES_ON_STARTUP        = True
REALLY_NUKE_SAVED_FILES_ON_STARTUP = True

SHOW_COLORED_LOGS = True
ALLOW_REGISTRATION = True
