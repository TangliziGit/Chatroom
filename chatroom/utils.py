import hashlib

from chatroom import config
from chatroom import database

def get_user_id():
    count=int(database.UserDatabase().count())
    return str(count+1)

def get_encrypt_password(password):
    salt=config.SALT
    password=password+salt
    password=hashlib.sha256(password.encode()).digest()
    return password

def check_password(password, true_password):
    password=get_encrypt_password(password)
    if password==true_password:
        return True
    return False

def get_room_id():
    count=int(database.ChatroomDatabase().count())
    return str(count+1)
