from flask import Flask
from flask_socketio import SocketIO
import chatroom.database

def create_app():
    app=Flask(__name__)
    app.config.from_pyfile('config.py')
    app.teardown_appcontext(chatroom.database.BaseDatabase.teardown)
    # app.cli.add_command()
    return app

def create_socket(app):
    socket=SocketIO(app)
    return socket
