from flask import Flask, request, Response

import os
import os.path
from os.path import join as pjoin
from datetime import datetime
import binascii
import threading
from functools import wraps
import time

import utils
import auth
import credentials as cred

import settings

import logging
import custom_logging
from custom_logging import Logging

app                                    = Flask(__name__)
logging.getLogger("werkzeug").handlers = []
logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
app.logger.handlers                    = []
app.logger.setLevel(logging.DEBUG)
logger                                 = Logging(app)
UPLOAD_DIR                             = pjoin(os.getcwd(), "uploads")
app.config['FLASK_LOG_LEVEL']          = 'INFO'

def get_basic_auth_creds():
    return (request.authorization.username,
            request.authorization.password)

@app.after_request
def post_request_logging(response):
    #Logging statement
    if response.status_code == 200:
        f = app.logger.info
    else:
        f = app.logger.error

    f('{} {} {} {}'.format(
        request.remote_addr,
        request.method,
        request.url,
        response.status,
        str(request.data)
     ))
    return response

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_auth(user, pw):
    try:
        if cred.get_pwdhash(user) == cred.kdf(str.encode(pw)):
            app.logger.debug("Successfully authenticated user {}".format(user))
            return True
        else:
            app.logger.error("Failed login attempt for user {}".format(user))
            return False

    except KeyError:
        app.logger.error("User {} not found!".format(user))
        return False

@app.route('/')
def home():
    return "Welcome"

@app.route('/upload', methods=['POST'])
def upload():
    # get the 'upload_file' field from the form
    uid, pwd = get_basic_auth_creds()
    
    if check_auth(uid, pwd):
        upload_file          = request.files.get(settings.FILE_UPLOAD_FIELD_NAME)
        user_rel_upload_path = request.form.get("path")
        user_dir             = pjoin(UPLOAD_DIR, uid)

        source_file               = upload_file.filename
        source_fname, source_fext = os.path.splitext(upload_file.filename)
        target_fname              = (source_fname
                + " (" + utils.current_timestamp() + ")" + source_fext)

        app.logger.debug("Received file {}".format(source_file))

        if not os.path.isdir(user_dir):
            app.logger.warn("Created dir /uploads/{0} for user {0}".format(uid))
            os.mkdir(user_dir)

        save_dir = pjoin(user_dir, user_rel_upload_path, source_file)

        if not os.path.isdir(save_dir):
            app.logger.debug("Created /uploads/{}".format(pjoin(uid,
                user_rel_upload_path)))
            os.makedirs(save_dir)

        save_path = pjoin(save_dir, target_fname)

        upload_file.save(save_path)
        app.logger.debug("Saved to /uploads/{}".format(pjoin(uid, 
            user_rel_upload_path, source_file, target_fname)))

        return "All done!"
    else:
        return Response("You must have a valid login to upload files.\n" \
                        "Please contact the system administrator.", 401)

@app.errorhandler(404)
def error404(err):
    return Response("Not found", 404)

def run_app():
    app.run(host='localhost', port=8080, debug=True)

if __name__ == '__main__':
    app.logger.info("Restarting server")
    run_app()
