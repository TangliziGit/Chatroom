import functools

from flask import (
    Blueprint, session, g, request, render_template, redirect,
    url_for, flash
)

import chatroom
from chatroom import config
from chatroom import utils
from chatroom.auth import login_required
from chatroom.database import *

bp=Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/createroom', methods=['POST'])
@login_required
def createroom():
    roomName=request.form['roomName']
    roomDescription=request.form['roomDescription']
    roomCapacity=int(request.form['roomCapacity'])

    room_db=ChatroomDatabase()
    error=None

    if roomCapacity>config.MAX_CAPACITY:
        error="Capacity can not over %d."%config.MAX_CAPACITY
    elif len(roomName)==0:
        error="Room name is required."
    elif room_db.find_one({
        'roomName': roomName
    }) is not None:
        error="Room `%s` has already be created."%roomName

    if error is None:
        room=Chatroom({
            'roomId': utils.get_room_id(),
            'roomName': roomName,
            'roomDescription': roomDescription,
            'roomCapacity': roomCapacity
        })
        room_db.insert(room)
        return redirect(url_for('chat.chatroom', roomId=room['roomId']))
    else:
        flash(error)
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@bp.route('/chatroom', methods=['GET'])
@login_required
def chatroom():
    roomId=request.args.get('roomId', None)

    room_db=ChatroomDatabase()
    room=room_db.find_one({
        'roomId': roomId
    })
    error=None

    if room is None:
        error="Room `%s` does not exit."%roomId

    if error is None:
        g.room=room
        session['userId']=g.user['userId']
        session['userName']=g.user['userName']
        session['roomId']=room['roomId']

        #print(session['userId']+session['roomId'])
        return render_template('chatroom.html')# , **room.roominfo)
    else:
        flash(error)
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))
