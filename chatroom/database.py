import hashlib
from pymongo import MongoClient
from flask import g

# attend this:
# you can not import a module like `import config`
# this would be wrong, because sys.path is not contain this path.
# you should import with a package name.
from chatroom import config
from chatroom import roomlist

class BaseDatabase:
    db=None
    con=None
    def __init__(self):
        self.con=None
        if 'con' not in g:
            self.con=MongoClient()
            g.con=self.con
        else:
            self.con=g.con

    @staticmethod
    def teardown(self):
        con=g.pop('con', None)
        if con is not None:
            con.close()

class UserDatabase(BaseDatabase):
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

    def remove(self, user_id):
        pass

    def update(self, user_id, user):
        pass

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
                db.update_by_id(self.userinfo["userId"], info)
            except:
                # err
                pass
            else:
                self.userinfo[key]=new_value
        else:
            # err
            pass


class MsgDatabase(BaseDatabase):
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

class ChatroomDatabase(BaseDatabase):
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
                'roomCapacity':         room['roomCapacity'],
                # 'password':         password,
            })

    def remove(self, room_id):
        pass

    def update(self, room_id, room):
        pass

    def find_one(self, query):
        res=list(self.db.find(query))
        if len(res)<1:
            return None
        res=res[0]
        res.pop("_id")
        # res.pop("password")
        room=Chatroom(res)
        return room

    def find(self, query, limit=1, skip=0):
        roomlist=[]
        for res in self.db.find(query)[skip:skip+limit]:
            res.pop("_id")
            # res.pop("password")
            room=Chatroom(res)
            roomlist.append(room)
        return roomlist

    def count(self, query={}):
        cnt=self.db.count_documents(query)
        return cnt

class Chatroom:
    roominfo={}
    userlist=None

    def __init__(self, roominfo):
        try:
            self.roominfo['roomId']=roominfo['roomId']
            self.roominfo['roomName']=roominfo['roomName']
            self.roominfo['roomDescription']=roominfo['roomDescription']
            self.roominfo['roomCapacity']=roominfo['roomCapacity']
        except KeyError as err:
            print("Error in init Chatroom instance.")
            print("KeyError: ", err)
        except AttributeError as err:
            print("Error in init Chatroom instance.")
            print("AttributeError:", err)
        else:
            pass
        self.userlist=UserList()

    def __getitem__(self, key):
        try:
            if self.roominfo.get(key, None):
                return self.roominfo[key]
        except AttributeError as err:
            print("Error in get roominfo.")
            print("AttributeError:", err)
        return None

    def __setitem__(self, key, new_value):
        db=ChatroomDatabase()
        if self.roominfo.get(key, None):
            try:
                info=self.roominfo
                info[key]=new_value
                db.update_by_id(self.roominfo["roomId"], info)
            except:
                # err
                pass
            else:
                self.roominfo[key]=new_value
        else:
            # err
            pass

    def append(self, user):
        self.userlist.append(user)

    def get_userlist(self):
        return self.userlist

    def remove(self, query):
        self.userlist.remove(query)

    def history(self, query={}, limit=1, skip=0):
        query['roomId']=str(self.room_id)
        res=Message.history(query)
        return res

    @staticmethod
    def get_room(roomId):
        if roomId not in roomlist:
            room_db=ChatroomDatabase()
            _room=room_db.find_one({
                'roomId': roomId
            })
            roomlist[roomId]=_room
        return roomlist[roomId]

class UserList:
    userlist=[]

    def __init__(self):
        pass

    def append(self, user):
        if not isinstance(user, User):
            return None
        self.userlist.append(user)
        self.dereplicate()

    def dereplicate(self):
        self.userlist=list(set(self.userlist))

    def remove(self, query):
        """
            params: 'query' is a dict, which can be followed to find items.
            exmaple:
                userlist.remove({'userName': 'admin'})
        """
        res=[]
        for key, value in query.items():
            res.extend([x for x in self.userlist if not x[key]==value])
        self.userlist=res

    def find(self, query={}):
        """
            params: 'query' is a dict, which can be followed to find items.
            exmaple:
                userlist.find({'userName': 'admin'})
        """
        res=[]
        for key, value in query.items():
            res.extend([x for x in self.userlist if x[key]==value])
        return tmplist
    
    def count(self):
        return len(self.userlist)
