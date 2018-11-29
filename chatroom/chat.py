import functools

from flask import (
    Blueprint, session, g, request, render_template, redirect,
    url_for, flash, send_from_directory
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
        room={
            'roomId': utils.get_room_id(),
            'roomName': roomName,
            'roomDescription': roomDescription,
            'roomCapacity': roomCapacity,
            'hostUserId': g.user['userId'],
            'hostUserName': g.user['userName']
        }
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
    room=ChatroomDatabase().find_one({'roomId': roomId})
    error=None

    if room is None:
        error="Room `%s` does not exit."%roomId
    # TODO
    # elif len(room['userlist'])>=room['roomCapacity']:
    #    error="Room `%s` is already full."%roomId

    if error is None:
        g.room=room
        session['userId']=g.user['userId']
        session['userName']=g.user['userName']
        session['userColorName']=g.user['userColorName']
        session['roomId']=room['roomId']
        # room_list.append(g.user['userId'], room['roomId'])

        return render_template('chatroom.html')
    else:
        flash(error)
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@bp.route('/roomlist', methods=['GET'])
def roomlist():
    # room_list=RoomList()
    rooms=ChatroomDatabase().find({})# room_list.get_all()
    print(rooms)
    rooms_dict={}
    for room in rooms:
        rooms_dict[room['roomId']]=room

    # socket_rooms=g.socket.server.manager.rooms.get('/chat', {})
    # for roomId in socket_rooms.keys():
    #     if roomId not in rooms_dict.keys():
    #         continue
    #     rooms_dict[roomId]['userlist']=list(socket_rooms[roomId].keys())

    rooms=[]
    for key, value in rooms_dict.items():
        rooms.append(value)

    return json.dumps(rooms);

@bp.route('/memberlist', methods=['GET'])
def memberlist():
    roomId=request.args.get('roomId', None)
    # room_list=RoomList()
    user_db=UserDatabase()
    room=None
    error=None

    if roomId is None:
        error='roomId is required.'
    else:
        room=ChatroomDatabase().find_one({
            'roomId': roomId
        })
        if room is None:
            error="Room `%s` does not exit."%roomId

    if error is None:
        userlist=[]
        for userId in room['userlist']:
            user=user_db.find_one({
                'userId': userId
            })
            userlist.append({
                'userId': userId,
                'userName': user['userName']
            })
        return json.dumps(userlist)
    else:
        return error

@bp.route('/filelist', methods=['GET'])
@login_required
def filelist():
    if 'roomId' not in session:
        return 'Please enter a chatroom firstly.'

    file_db=FileDatabase()
    filelist=file_db.find({
        'holdRoomId': session['roomId']
    })

    file_info_list=[]
    for x in filelist:
        file_info_list.append(x.fileinfo)

    return json.dumps(file_info_list)

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    roomId=request.form['roomId']
    file_=request.form['file']
    file_db=FileDatabase()
    error=None

    if file_ is None:
        error='File is required.'
    elif 'roomId' not in session:
        error='Please enter a chatroom firstly.'
    # elif file_.size()>...:
    #     error='...'

    if error is None:
        fileName=secure_filename(file_.filename)
        isdone=file_db.insert({
            'fileId':           utils.get_file_id(),
            'fileName':         fileName,
            'filePath':         utils.get_file_path(fileName),
            'holdRoomId':       roomId,
            'holdUserId':       session['userId'],
            'uploadTimeStamp':  utils.get_time(),
            'downloadCount':    '0'
        }, file_)
        if isdone:
            return 'Upload successfully.'
        else:
            return 'Upload failed.'
    else:
        return error

@bp.route('/download', methods=['GET'])
@login_required
def download():
    fileId=request.arg.get('fileId', None)
    file_db=FileDatabase()
    error=None

    if fileId is None:
        error='Please select a file.'
    elif file_db.fild_one({
        'fileId': fileId
    }) is None:
        error='File `%d` does not exit.'

    if error is None:
        file_=file_db.find_one({
            'fileId': fileId
        })
        return send_from_directory(config.FILE_PREFIX, file_['filePath'], as_attendment=True)
    else:
        return error
