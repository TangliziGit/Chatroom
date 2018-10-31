import hashlib
import json
import time
from pymongo import MongoClient
from redis import StrictRedis
from flask import g

# attend this:
# you can not import a module like `import config`
# this would be wrong, because sys.path is not contain this path.
# you should import with a package name.
from chatroom import config
from chatroom import mongo_con, redis_con

class MongoBaseDatabase:
    db=None
    con=None
    def __init__(self):
        self.con=None
        if 'mongo_con' not in g:
            print("Error: g.mongo_con is None")
            # self.con=MongoClient()
            self.con=mongo_con
            g.mongo_con=self.con
        else:
            self.con=g.mongo_con

    @staticmethod
    def teardown(exception):
        con=g.pop('con', None)
        if con is not None:
            con.close()

class UserDatabase(MongoBaseDatabase):
    def __init__(self):
        super(UserDatabase, self).__init__()
        self.db=None
        if 'user_db' not in g:
            self.db=self.con.Chatroom.users
            g.user_db=self.db
        else:
            self.db=g.user_db

    def insert(self, user, password):
        res=list(self.db.find({'userId': user['userId']}))
        if len(res)!=0:
            pass
        else:
            self.db.insert({
                'userId': user['userId'],
                'userName': user['userName'],
                'userProfile': user['userProfile'],
                'password': password,
            })

    def remove(self, userId):
        self.db.remove({
            'userId': userId
        })

    def update(self, userId, new_user, new_password):
        self.remove(userId)
        self.insert(new_user, new_password)

    def find_one(self, query):
        res=list(self.db.find(query))
        if len(res)<1:
            return None
        res=res[0]
        res.pop("_id")
        res.pop("password")
        user=User(res)
        return user

    def find_one_with_password(self, query):
        res=list(self.db.find(query))
        if len(res)<1:
            return None
        res=res[0]
        res.pop("_id")
        password=res.pop("password")
        user=User(res)
        return user, password

    def find(self, query, limit=1, skip=0):
        userlist=[]
        for res in self.db.find(query)[skip:skip+limit]:
            res.pop("_id")
            res.pop("password")
            user=User(res)
            userlist.append(user)
        return userlist

    def count(self, query={}):
        cnt=self.db.count_documents(query)
        return cnt

class User:
    userinfo={}

    def __init__(self, userinfo):
        try:
            self.userinfo['userId']=userinfo['userId']
            self.userinfo['userName']=userinfo['userName']
            self.userinfo['userProfile']=userinfo['userProfile']
        except KeyError as err:
            print("Error in init User instance.")
            print("KeyError: ", err)
        except AttributeError as err:
            print("Error in init User instance.")
            print("AttributeError:", err)
        else:
            pass

    def __getitem__(self, key):
        try:
            if self.userinfo.get(key, None):
                return self.userinfo[key]
        except AttributeError as err:
            print("Error in get userinfo.")
            print("AttributeError:", err)
        return None

    def __setitem__(self, key, new_value):
        db=UserDatabase()
        if self.userinfo.get(key, None):
            try:
                info=self.userinfo
                info[key]=new_value
                db.update(self.userinfo["userId"], info)
            except:
                # err
                pass
            else:
                self.userinfo[key]=new_value
        else:
            # err
            pass


class MsgDatabase(MongoBaseDatabase):
    def __init__(self):
        super(MsgDatabase, self).__init__()
        self.db=None
        if 'msg_db' not in g:
            self.db=self.con.Chatroom.messages
            g.msg_db=self.db
        else:
            self.db=g.msg_db

    def insert(self, message):
        res=list(self.db.find({'messageId': message['messageId']}))
        if len(res)!=0:
            pass
        else:
            self.db.insert({
                'messageId': message['messageId'],
                'userId': message['userId'],
                'roomId': message['roomId'],
                'messageTimeStamp': message['messageTimeStamp'],
                'messageContent': message['messageContent']
            })

    def remove(self, msg_id):
        pass

    def update(self, msg_id, message):
        pass

    def find_one(self, query):
        res=list(self.db.find(query))
        if len(res)<1:
            return None
        res=res[0]
        res.pop("_id")
        msg=Message(res)
        return msg

    def find(self, query, limit, skip):
        msglist=[]
        for res in self.db.find(query)[skip:skip+limit]:
            res.pop("_id")
            msg=Message(res)
            msglist.append(msg)
        return msglist
        
    def count(self, query={}):
        cnt=self.db.count_documents(query)
        return cnt

class Message:
    msginfo={}

    def __init__(self, msginfo):
        try:
            self.msginfo['messageId']=msginfo['messageId']
            self.msginfo['userId']=msginfo['userId']
            self.msginfo['roomId']=msginfo['roomId']
            self.msginfo['messageTimeStamp']=msginfo['messageTimeStamp']
            self.msginfo['messageContent']=msginfo['messageContent']
        except KeyError as err:
            print("Error in init Msg instance.")
            print("KeyError:", err)
        except AttributeError as err:
            print("Error in init Msg instance.")
            print("AttributeError:", err)
        else:
            pass

    def __getitem__(self, key):
        try:
            if self.msginfo.get(key, None):
                return self.msginfo[key]
        except AttributeError as err:
            print("Error in get msginfo.")
            print("AttributeError:", err)
        return None

    def __setitem__(self, key, new_value):
        db=MsgDatabase()
        if msginfo.get(key, None):
            try:
                info=self.msginfo
                info[key]=new_value
                db.update(self.msginfo['messageId'], info)
            except:
                # err
                pass
            else:
                self.msginfo[key]=new_value
        else:
            # err
            pass

    @staticmethod
    def history(query={}, limit=1, skip=0):
        """
            params: 'query' is a dict, which can be followed to find items.
            exmaple:
                Message.find({'userName': 'admin', 'messageTimeStamp': {'$gt': '1'}})
        """
        db=MsgDatabase()
        res=db.find(query, limit, skip)
        return res

class ChatroomDatabase(MongoBaseDatabase):
    def __init__(self):
        super(ChatroomDatabase, self).__init__()
        self.db=None
        if 'room_db' not in g:
            self.db=self.con.Chatroom.rooms
            g.room_db=self.db
        else:
            self.db=g.room_db

    def insert(self, room): #, password):
        res=list(self.db.find({'roomId': room['roomId']}))
        if len(res)!=0:
            pass
        else:
            self.db.insert({
                'roomId':           room['roomId'],
                'roomName':         room['roomName'],
                'roomDescription':  room['roomDescription'],
                'roomCapacity':     room['roomCapacity'],
                'hostUserId':       room['hostUserId'],
                'hostUserName':     room['hostUserName']
                # 'password':         password,
            })

    def remove(self, room_id):
        pass

    def update(self, room_id, room):
        pass

    def find_one(self, query):
        res=list(self.db.find(query))
        if len(res)==0:
            return None
        room=res[0]
        room.pop("_id")
        # res.pop("password")
        room['userlist']=[]
        return room

    def find(self, query, limit=1, skip=0):
        rooms=[]
        roomlist=RoomList()
        for room in self.db.find(query)[skip:skip+limit]:
            room.pop('_id')
            online_room=roomlist.get(room['roomId'])

            if online_room is not None:
                room=online_room
            else:
                room['userlist']=[]
            rooms.append(room)
        return rooms

    def count(self, query={}):
        cnt=self.db.count_documents(query)
        return cnt

class RedisBaseDatabase:
    db=None
    def __init__(self):
        if 'redis_con' not in g:
            # print("Error: g.redis_con is None")
            g.redis_con=redis_con
        self.db=g.redis_con

    @staticmethod
    def teardown(exception):
        pass

class RoomList(RedisBaseDatabase):
    def __init__(self):
        super(RoomList, self).__init__()

    def get(self, roomId):
        room=self.db.get("Chatroom:Room:"+roomId)
        if room is None:
            room=ChatroomDatabase().find_one({'roomId': roomId})
            self.set(roomId, room)
            return room
        else:
            room=json.loads(room)
            return room

    # need test
    def get_all(self):
        rooms=[]
        for key in self.db.keys():
            key=key.decode()
            if "Chatroom:Room:" not in key:
                continue
            room=self.db.get(key).decode()
            room=json.loads(room)
            room['userlist']=[]
            rooms.append(room)
        return rooms

    def set(self, roomId, roominfo):
#       'roomId'
#       'roomName'
#       'roomDescription'
#       'roomCapacity'
#       'hostUserId'
#       'userlist': [userid, ...]
        # need to judge
        room=json.dumps(roominfo)
        self.db.set("Chatroom:Room:"+roomId, room)
    
    def append(self, userId, roomId):
        room=self.get(roomId)
        room['userlist'].append(userId)
        room['userlist']=list(set(room['userlist']))
        self.set(roomId, room)

    def remove(self, userId, roomId):
        room=self.get(roomId)
        room['userlist'].remove(userId)
        self.set(roomId, room)

class FileDatabase(MongoBaseDatabase):
    def __init__(self):
        super(FileDatabase, self).__init__()
        self.db=None
        if 'file_db' not in g:
            self.db=self.con.Chatroom.files
            g.file_db=self.db
        else:
            self.db=g.file_db

    def insert(self, file_, file_self):
        try:
            res=list(self.db.find({'fileId': file_['fileId']}))
            if len(res)!=0:
                return False
            file_self.save(file_['filePath'])
            return False
        except:
            self.db.insert({
                'fileId':           file_['fileId'],
                'fileName':         file_['fileName'],
                'filePath':         file_['filePath'],
                'holdRoomId':       file_['holdRoomId'],
                'holdUserId':       file_['holdUserId'],
                'uploadTimeStamp':  file_['uploadTimeStamp'],
                'downloadCount':    file_['downloadCount']
            })
            return True

    def remove(self, fileId):
        file_=self.db.find_one(fileId)
        path=os.path.join(config.FILE_PREFIX, file_['filePath'])
        os.remove(path)
        self.db.remove({
            'fileId': fileId
        })

    # def update(self, userId, new_user, new_password):
    #     self.remove(userId)
    #     self.insert(new_user, new_password)

    def find_one(self, query):
        res=list(self.db.find(query))
        if len(res)<1:
            return None
        res=res[0]
        res.pop("_id")
        res.pop("filePath")
        file_=File(res)
        return file_

    def find(self, query, limit=1, skip=0):
        filelist=[]
        for res in self.db.find(query)[skip:skip+limit]:
            res.pop("_id")
            res.pop("filePath")
            file_=File(res)
            filelist.append(file_)
        return filelist

    def count(self, query={}):
        cnt=self.db.count_documents(query)
        return cnt

class File:
    fileinfo={}

    def __init__(self, userinfo):
        try:
            self.fileinfo['fileId']=fileinfo['fileId']
            self.fileinfo['fileName']=fileinfo['fileName']
            # self.fileinfo['filePath']=fileinfo['filePath']
            self.fileinfo['holdRoomId']=fileinfo['holdRoomId']
            self.fileinfo['holdUserId']=fileinfo['holdUserId']
            self.fileinfo['uploadTimeStamp']=fileinfo['uploadTimeStamp']
            self.fileinfo['downloadCount']=fileinfo['downloadCount']
        except KeyError as err:
            print("Error in init File instance.")
            print("KeyError: ", err)
        except AttributeError as err:
            print("Error in init File instance.")
            print("AttributeError:", err)
        else:
            pass

    def __getitem__(self, key):
        try:
            if self.fileinfo.get(key, None):
                return self.fileinfo[key]
        except AttributeError as err:
            print("Error in get fileinfo.")
            print("AttributeError:", err)
        return None
