from redis import StrictRedis
from pymongo import MongoClient

from flask import (
    Flask, render_template, redirect, g
)
from flask_socketio import SocketIO


mongo_con=MongoClient()
redis_con=StrictRedis()

from chatroom import auth
from chatroom import user
from chatroom import chat
from chatroom import database

def create_app_socket():
    app=Flask(__name__)
    app.config.from_pyfile('config.py')
    app.teardown_appcontext(database.MongoBaseDatabase.teardown)
    app.teardown_appcontext(database.RedisBaseDatabase.teardown)
    socket=SocketIO(app)
    # app.cli.add_command()

    @app.before_request
    def connect_db():
        g.mongo_con=mongo_con
        g.redis_con=redis_con
        g.socket=socket

    @app.route('/index', methods=['GET'])
    def index(**kwargs):
        if g.user is not None:
            g.registerTime=utils.to_date(g.user['registerTime'])
            g.lastSeenTime=utils.to_date(g.user['lastSeenTime'])
        return render_template('index.html', colors=config.COLOR, **kwargs)

    @app.route('/', methods=['GET'])
    def root():
        return redirect('/index')

    @app.errorhandler(404)
    def page_not_find(error):
        return render_template('404.html'), 404

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(chat.bp)

    return (app, socket)

app, socket=create_app_socket()

from chatroom import events
