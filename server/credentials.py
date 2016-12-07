from hashlib import pbkdf2_hmac
import codecs
import json
import settings
import os


def hash_kdf(pw):
    return codecs.encode(
        pbkdf2_hmac('sha256', str.encode(pw), b'salt', 10000),
        'hex').decode('utf-8')


DB_PATH = os.path.join(os.getcwd(), "db.json")


class CredentialManager(object):
    def __init__(self, logger=None):
        self.logger = logger
        self.logger.debug("Starting credential manager module")
        self.db = dict()
        self.update_db()

    def update_db(self):
        try:
            with open(DB_PATH) as _file:
                db_ = json.load(_file)
                if db_ != self.db:
                    if self.logger:
                        self.logger.debug("Updating database")
                    self.db = db_
        except FileNotFoundError:
            self.logger.debug("Database not found, creating a new one.")
            # Create the database.
            self.db['users'] = []
            self.db['hashes'] = dict()
            self.persist_db_to_file()

    def persist_db_to_file(self):
        with open(DB_PATH, "w") as _file:
            json.dump(self.db, _file)

    def get_pwdhash(self, user):
        return self.db['hashes'][user]

    def get_users(self):
        return self.db['users']

    def set_pwdhash(self, user, pwd_hash):
        if user in self.db['users']:
            self.logger.debug("Setting new password for {}".format(user))
            self.db['hashes'][user] = pwd_hash
        else:
            self.logger.debug("Unauthorized user {}!".format(user))
        self.persist_db_to_file()

    def authenticate(self, user, pw):
        self.update_db()
        if user in self.db['users']:
            if self.get_pwdhash(user) == hash_kdf(pw):
                return True
            else:
                self.logger.critical("expected {}, got {}".format(
                    self.get_pwdhash(user), hash_kdf(pw)))
        elif settings.ALLOW_REGISTRATION:
            self.logger.debug("Registered new user {}".format(user))
            self.db['users'].append(user)
            self.set_pwdhash(user, hash_kdf(pw))
            return True
        return False
