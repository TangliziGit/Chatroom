# TODO:
#  0. disconnect problem
#  1. deal with secure problems
#  2. maybe more beautiful?

import json, time, random

from flask import *
from flask_socketio import SocketIO, join_room, leave_room, emit
from itsdangerous import Serializer
from urllib import parse

from pymongo import MongoClient

import config

app=Flask(__name__)
app.config.from_object(config)
socketio=SocketIO(app)
signer=Serializer(config.SECRET_KEY)

mdb=MongoClient().ChatRoom.messages
idset=set([])

def get_time():
    return round(time.time()*1000)

def get_random_id():
    rand_value=random.randint(1, 9999)
    while rand_value in idset:
        rand_value=random.randint(1, 9999)
    idset.add(rand_value)
    return ("%s"%(rand_value)).zfill(4)

def get_sign_items(signed):
    try:
        sign=signer.loads(signed)
    except:
        return None
    else:
        return sign

@socketio.on('connect', namespace='/chat')
def on_connect():
    signed=request.cookies.get('ChatRoomSign', 0)
    sign=get_sign_items(signed)
    
    if isinstance(sign, dict):
        join_room(sign['room_id'])
        room_info={'user_id':   sign['user_id'],
                   'user_name': sign['user_name'],
                   'ifenter':   True
        }
        emit('room_info', room_info, room=sign['room_id'], broadcast=True)

@socketio.on('submit', namespace='/chat')
def on_submit(message):
    signed=request.cookies.get('ChatRoomSign', 0)
    sign=get_sign_items(signed)

    if isinstance(sign, dict):
        emitmsg={'user_id':     sign['user_id'],
                 'user_name':   sign['user_name'],
                 'content':     escape(parse.unquote(message['content']))
        }

        mdb.insert({
            'user_id':      sign['user_id'],
            'user_name':    sign['user_name'],
            'room_id':      sign['room_id'],
            'content':      message['content']
        })
        emit('message', emitmsg, room=sign['room_id'], broadcast=True)

@app.errorhandler(404)
def page_not_find(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def index():
    signed=request.cookies.get('ChatRoomSign', 0)
    sign=get_sign_items(signed)
    
    if isinstance(sign, dict):
        return render_template('index.html', user_name=sign['user_name'])
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    signed=request.cookies.get('sign', 0)
    sign=get_sign_items(signed)
    if isinstance(sign, dict):
        return redirect('index')

    if request.method=='POST':
        form=request.form
        user_name=request.form.get('userName', None)
        room_id=form.get('room_id', 0)

        if not form or not user_name:
            return render_template('login.html', info="not entered user name.")
        else:
            sign=signer.dumps({
                "user_id":      get_random_id(),
                "user_name":    user_name,
                "room_id":      room_id,
            })
            resp=make_response(redirect('/'))
            resp.set_cookie("ChatRoomSign", sign)
            return resp
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    signed=request.cookies.get('sign', 0)
    sign=get_sign_items(signed)

    if isinstance(sign, dict) and sign['user_id'] in idset:
        idset.remove(sign['user_id'])
    resp=make_response(redirect('/login'))
    resp.delete_cookie("ChatRoomSign")
    return resp

if __name__=='__main__':
    app.run(port=config.WEB_PORT)
    # app.run(config.WEB_ADDR, port=config.WEB_PORT)
