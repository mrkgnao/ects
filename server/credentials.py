from hashlib import pbkdf2_hmac 
import codecs
import json

def hash_kdf(pw):
    return codecs.encode(
            pbkdf2_hmac('sha256', str.encode(pw), b'salt', 10000), 'hex').decode('utf-8')

# if user folders don't exist create them
db = dict()
with open("db.json") as _file:
    db = json.load(_file)

def update_db():
    with open("db.json") as _file:
        db = json.load(_file)

def get_pwdhash(user):
    update_db()
    return db['hashes'][user]

def get_users():
    update_db()
    return db['users']

def set_pwdhash(user, pw):
    update_db()
    if user in db['users']:
        db['hashes'][user] = hash_kdf(pw)
        with open("db.json", "w") as _file:
            json.dump(db, _file)
    else:
        print("Unauthorized user {}!".format(user))

def authenticate(user, pw):
    update_db()
    if user in db['users']:
        if get_pwdhash(user) == hash_kdf(pw):
            return True
    return False
