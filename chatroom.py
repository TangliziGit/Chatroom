# TODO:
# 0. deal with disconnect problem
# 1. deal with secure problems
# 2. maybe more beautiful?

import json, time, random

from flask import *
from flask_socketio import SocketIO, join_room, leave_room, emit
from pymongo import MongoClient

import config

app=Flask(__name__)
app.config.from_object(config)
socketio=SocketIO(app)

mcol=MongoClient().ChatRoom.messages
idset=set([])

def get_time():
    return round(time.time()*1000)

def get_random_id():
    rand_value=random.randint(1, 9999)
    while rand_value in idset:
        rand_value=random.randint(1, 9999)
    idset.add(rand_value)
    return ("%s"%(rand_value)).zfill(4)

@socketio.on('connect', namespace='/chat')
def on_connect():
    join_room(session.get('room_id', 0))

    room_info={'user_id':   session['user_id'],
               'user_name': session['user_name'],
               'ifenter':   True}
    emit('room_info', room_info, room=session['room_id'], broadcast=True)


@socketio.on('submit', namespace='/chat')
def on_submit(message):
    emitmsg={'user_id':     session['user_id'],
             'user_name':   session['user_name'],
             'content':     escape(message['content']),
            }
    emit('message', emitmsg, room=session['room_id'], broadcast=True)

@app.errorhandler(404)
def page_not_find(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def index():
    if session.get('user_id', None):
        return render_template('index.html', user_name=session['user_name'])
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id', None):
        return redirect('/')
    if request.method=='POST':
        form=request.form
        username=request.form.get('userName', None)
        room_id=form.get('room_id', 0)

        if not form or not username:
            return render_template('login.html', info="not entered user name.")
        else:
            session['room_id']=room_id
            session['user_id']=get_random_id()
            session['user_name']=escape(username)

            return redirect('/')
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    user_id=session.get('user_id', '')
    if user_id in idset:
        idset.remove(user_id)
    # leave_room(session.get('room_info', 0))
    session.pop('room_id', None)
    session.pop('user_id', None)
    session.pop('user_name', None)

    # room_info={'user_id':   session['user_id'],
    #            'user_name': session['user_name'],
    #            'ifenter':   False}
    # emit('room_info', room_info, room=session['room_id'])

    return redirect('/login')

if __name__=='__main__':
    app.run()
