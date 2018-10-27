# Chatroom
A simple chatroom practice project, which uses flask, mongodb and redis.

# Functions
- /auth
    - /register
    - /login
    - /logout
- /chat
    - /createroom
    - /chatroom
    - /roomlist     
    - /memberlist   (unvaild)
    - /filelist
    - /upload       (not tested)
    - /download     (not tested)
- /user
    - /detail
    - /update       (not tested)
- socket
    - join
    - submit
    - leave

# TODO
0. test
1. database
    - ! maintain a sessionId to session db.
    - ! clear unvalid session according to time.(per hour)
2. websocket
    - ! maintain real-time userlist for each room.
2. http
    - chatroom operations(update, remove, etc.)
    - user operations(update, remove, etc.)
3. upload files
4. ? message with pictures
5. ? calendar data

## more
1. use pytest to test each module
2. use click
3. use gunicorn
