import hashlib
from pymongo import MongoClient
from flask import g

# attend this:
# you can not import a module like `import config`
# this would be wrong, because sys.path is not contain this path.
# you should import with a package name.
import chatroom.config

class BaseDatabase:
    db=None
    def __init__(self):
        self.con=None
        if 'con' not in g:
            self.con=MongoClient()
        else:
            self.con=g['con']

    @staticmethod
    def teardown(self):
        con=g.pop('con', None)
        if con is not None:
            con.close()

class UserDatabase(BaseDatabase):
    def __init__(self):
        super(UserDatabase, self).__init__()
        self.db=self.con.Chatroom.users

    def insert(self, user, password):
        res=list(self.db.find({'userId': user['userId']}))
        if len(res)!=0:
            pass
        else:
            self.db.insert({
                'userId': user['userId'],
                'name': user['name'],
                'password': self.__encrypt_with_salt(password),
                'profile': user['profile']
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

    def find(self, query, limit, skip):
        userlist=[]
        for res in self.db.find(query)[skip:skip+limit]:
            res.pop("_id")
            res.pop("password")
            user=User(res)
            userlist.append(User)
        return userlist

    def __encrypt_with_salt(self, password):
        salt=config.SALT
        password=password+salt
        # attend this
        password=hashlib.sha256(password.encode()).digest()
        return password

class User:
    userinfo={}

    def __init__(self, userinfo):
        try:
            self.userinfo['userId']=userinfo['userId']
            self.userinfo['name']=userinfo['name']
            self.userinfo['profile']=userinfo['profile']
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
        self.db=self.con.Chatroom.messages

    def insert(self, message):
        res=list(self.db.find({'msgId': message['msgId']}))
        if len(res)!=0:
            pass
        else:
            self.db.insert({
                'msgId': message['msgId'],
                'userId': message['userId'],
                'roomId': message['roomId'],
                'timeStamp': message['timeStamp'],
                'content': message['content']
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
        
class Message:
    msginfo={}

    def __init__(self, msginfo):
        try:
            self.msginfo['msgId']=msginfo['msgId']
            self.msginfo['userId']=msginfo['userId']
            self.msginfo['roomId']=msginfo['roomId']
            self.msginfo['timeStamp']=msginfo['timeStamp']
            self.msginfo['content']=msginfo['content']
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
                db.update(self.msginfo['msgId'], info)
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
                Message.find({'name': 'admin', 'timeStamp': {'$gt': '1'}})
        """
        db=MsgDatabase()
        # if query.get('time', None):
        #     query['timeStamp']={'$gt': time}
        #     res=db.find(
        #         query, # {'timeStamp': {'$gt': time}},
        #         limit,
        #         skip
        #     )
        # else:
        #     res=db.find(query, limit, skip)
        res=db.find(query, limit, skip)
        return res

class Chatroom:
    room_id=0
    userlist=None

    def __init__(self, room_id):
        self.room_id=room_id
        self.userlist=UserList()

    def append(self, user):
        self.userlist.append(user)

    def get_userlist(self):
        return self.userlist

    def remove(self, query):
        self.userlist.remove(query)

    def history(self, query={}, limit=1, skip=0):
        # db=MsgDatabase()
        # if time:
        #     res=db.find(
        #         {'timeStamp': {'$gt': time}, 'roomId': room_id},
        #         limit,
        #         skip
        #     )
        # else:
        #     res=db.find({'roomId': room_id},
        #         limit, skip
        #     )
        # return res
        query['roomId']=str(self.room_id)
        res=Message.history(query)
        return res

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
                userlist.remove({'name': 'admin'})
        """
        res=[]
        for key, value in query.items():
            res.extend([x for x in self.userlist if not x[key]==value])
        self.userlist=res

    def find(self, query={}):
        """
            params: 'query' is a dict, which can be followed to find items.
            exmaple:
                userlist.find({'name': 'admin'})
        """
        res=[]
        for key, value in query.items():
            res.extend([x for x in self.userlist if x[key]==value])
        return tmplist
    
    def count(self):
        return len(self.userlist)
