"""
    Test for:
        User, Message, UserDatabase, MsgDatabase
        Chatroom, UserList
"""

import sys
sys.path.append('../')

import chatroom
from chatroom.database import *

app=chatroom.create_app()
with app.test_request_context():
    # User:
    # __init__
    # UserDatabase:
    # __init__, insert, find
    udb=UserDatabase()
    test_user=User({'userId': '1', 'name': 'TestUser', 'profile': "Just for test."})
    udb.insert(test_user, password='testing')
    user=udb.find({'name': 'TestUser'}, 1, 0)
    print(user)

    # Message:
    # __init__, history
    # MsgDatabase:
    # __init__, find_one, insert
    mdb=MsgDatabase()
    msg=Message({
        'msgId': '1',
        'userId': '1',
        'roomId': '1',
        'timeStamp': '1011',
        'content': "first commit"
    })
    mdb.insert(msg)
    msg=mdb.find_one({'msgId': '1'})
    msg=Message.history({'userId': '1'})
    print(msg[0]['content'])

    # Chatroom:
    # __init__, append, get_userlist, remove, history
    # UserList:
    # __init__, count, remove, append
    room=Chatroom(1)
    room.append(test_user)
    print(room.get_userlist().count())
    room.remove({'userId': test_user['userId']})
    print(room.get_userlist().count())
    print(room.history())

    userlist=UserList()
    userlist.append(test_user)
    print(userlist.count())
    userlist.append(test_user)
    print(userlist.count())
    userlist.remove({'userId': test_user['userId']})
    print(userlist.count())

