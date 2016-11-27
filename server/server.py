#!/usr/bin/env python
from flask import Flask, request, Response, g

import os
import os.path
from os.path import join as pjoin
from functools import wraps
import time

import credentials as cred

import settings

import logging
from custom_logging import Logging

app = Flask(__name__)
logging.getLogger("werkzeug").handlers = []

# CRITICAL is 50.
# This kills the logger.
logging.getLogger("werkzeug").setLevel(100)
app.logger.setLevel(logging.DEBUG)

app.logger.handlers = []
logger = Logging(app)
UPLOAD_DIR = pjoin(os.getcwd(), "uploads")
app.config['FLASK_LOG_LEVEL'] = 'INFO'


def get_basic_auth_creds():
    return (request.authorization.username, request.authorization.password)


@app.before_request
def pre_request():
    g.start = time.clock()


@app.after_request
def post_request_logging(response):
    # Logging statement
    if response.status_code == 200:
        f = app.logger.info
    else:
        f = app.logger.error

    f('{} {} {} {} ({} ms)'.format(request.remote_addr, request.method,
                                   request.url, response.status,
                                   int(1000 * (time.clock() - g.start))))
    return response


def requires_auth(f):
    def authenticate():
        """Sends a 401 response that enables basic auth"""
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def check_auth(user, pw):
    try:
        if cred.authenticate(user, pw):
            app.logger.debug("Successfully authenticated user {}".format(user))
            return True
        else:
            app.logger.error("Failed login attempt for user {}".format(user))
            return False
    except KeyError:
        if user in cred.get_users():
            cred.set_pwdhash(user, cred.hash_kdf(pw))
            app.logger.debug("Added password for user {}".format(user))
            return True
        else:
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
        upload_file = request.files.get(settings.FILE_UPLOAD_FIELD_NAME)
        if upload_file is not None:
            user_rel_upload_path = request.form.get("path")
            user_dir = pjoin(UPLOAD_DIR, uid)

            source_file = upload_file.filename
            source_fname, source_fext = os.path.splitext(upload_file.filename)
            target_fname = request.content_md5 + source_fext

            app.logger.debug("Received file {}".format(source_file))

            if not os.path.isdir(user_dir):
                app.logger.warn("Created dir /uploads/{0} for user {0}".format(
                    uid))
                os.mkdir(user_dir)

            save_dir = pjoin(user_dir, user_rel_upload_path, source_file)

            if not os.path.isdir(save_dir):
                app.logger.debug("Created /uploads/{}".format(
                    pjoin(uid, user_rel_upload_path)))
                os.makedirs(save_dir)

            save_path = pjoin(save_dir, target_fname)
            if not os.path.exists(save_path):
                upload_file.save(save_path)
                app.logger.debug("Saved to /uploads/{}".format(
                    pjoin(uid, user_rel_upload_path, source_file, target_fname)))
            else:
                app.logger.debug("File md5 hasn't changed, skipping")

            return "All done!"
        else:
            return Response("You must have a valid login to upload files.\n"
                            "Please contact the system administrator.", 401)
    else:
        return Response("No file received for upload. Please try again.", 200)


@app.errorhandler(404)
def error404(err):
    return Response("Not found", 404)


@app.errorhandler(405)
def error405(err):
    return Response("It doesn't work that way ;)", 405)


@app.errorhandler(401)
def error401(err):
    return Response("Bugger off", 401)


def run_app():
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    app.logger.info("Restarting server")
    run_app()
