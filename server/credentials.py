from hashlib import pbkdf2_hmac
import codecs
import json
import settings


def hash_kdf(pw):
    return codecs.encode(
        pbkdf2_hmac('sha256', str.encode(pw), b'salt', 10000),
        'hex').decode('utf-8')


class CredentialManager(object):
    def __init__(self, logger=None):
        self.logger = logger
        if self.logger:
            self.logger.info("Starting credential manager module")
        self.db = dict()
        self.update_db()

    def update_db(self):
        if self.logger:
            self.logger.info("Updating database")
        with open("db.json") as _file:
            self.db = json.load(_file)

    def persist_db_to_file(self):
        with open("db.json", "w") as _file:
            json.dump(self.db, _file)

    def get_pwdhash(self, user):
        return self.db['hashes'][user]

    def get_users(self):
        return self.db['users']

    def set_pwdhash(self, user, pwd_hash):
        if settings.ALLOW_REGISTRATION:
            self.logger.info("Registered new user {}".format(user))
            self.db['hashes'][user] = pwd_hash
        elif user in self.db['users']:
            self.logger.info("Setting new password for {}".format(user))
            self.db['hashes'][user] = pwd_hash
        else:
            self.logger.info("Unauthorized user {}!".format(self, user))
        self.persist_db_to_file()

    def authenticate(self, user, pw):
        self.update_db()
        if user in self.db['users']:
            if self.get_pwdhash(user) == hash_kdf(pw):
                return True
            else:
                self.logger.info("expected {}, got {}".format(
                    self.get_pwdhash(user), hash_kdf(pw)))
        return False
