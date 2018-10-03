from flask import Flask
from flask_socketio import SocketIO

from chatroom import database
from chatroom import auth

def create_app():
    app=Flask(__name__)
    app.config.from_pyfile('config.py')
    app.teardown_appcontext(database.BaseDatabase.teardown)
    # app.cli.add_command()
    app.register_blueprint(auth.bp)
    return app

def create_socket(app):
    socket=SocketIO(app)
    return socket
