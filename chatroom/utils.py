import hashlib
import time
import os
import re

from chatroom import config
from chatroom import database

def get_user_id():
    count=int(database.UserDatabase().count())
    return str(count)

def get_room_id():
    count=int(database.ChatroomDatabase().count())
    return str(count)

def get_message_id():
    count=int(database.MsgDatabase().count())
    return str(count)

def get_file_id():
    count=int(database.FileDatabase().count())
    return str(count)

def get_file_path(filename):
    return os.path.join(config.FILE_PREFIX, filename)

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

def get_time():
    return int(time.time())

def get_color_code(color_name):
    return config.COLOR.get(color_name, None)

def check_email_availability(address):
    return re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', address)
