from hashlib import pbkdf2_hmac 

def kdf(pw):
    return pbkdf2_hmac('sha256', pw, b'salt', 10000)

HASHES = {"soham" : kdf(b'lol'),
          "arjo"  : kdf(b'elon'),
          "dude"  : kdf(b'dude')}

# TODO
# if user folders don't exist create them

def get_pwdhash(user):
    return HASHES[user]

