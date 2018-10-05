"""
    Test for:
        /auth/register
        /auth/login
        /auth/logout
"""

import sys, os
upper_path=os.path.realpath(__file__).split('/')
upper_path='/'.join(upper_path[:len(upper_path)-2])
sys.path.append(upper_path)

from flask import g

import chatroom
from chatroom import config

app=chatroom.create_app()

if __name__=='__main__':
    app.run(config.WEB_ADDR, port=config.WEB_PORT)
