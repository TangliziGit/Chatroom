from redis import StrictRedis
from pymongo import MongoClient

from flask import (
    Flask, render_template, g
)
from flask_socketio import SocketIO


mongo_con=MongoClient()
redis_con=StrictRedis()

from chatroom import auth
from chatroom import user
from chatroom import chat
from chatroom import database

def create_app():
    app=Flask(__name__)
    app.config.from_pyfile('config.py')
    app.teardown_appcontext(database.MongoBaseDatabase.teardown)
    app.teardown_appcontext(database.RedisBaseDatabase.teardown)
    # app.cli.add_command()

    @app.before_request
    def connect_db():
        if 'mongo_con' not in g:
            g.mongo_con=mongo_con
        if 'redis_con' not in g:
            g.redis_con=redis_con

    @app.route('/index', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_find(error):
        return render_template('404.html'), 404

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(chat.bp)

    return app

def create_socket(app):
    socket=SocketIO(app)
    return socket

app=create_app()
socket=create_socket(app)

from chatroom import events
