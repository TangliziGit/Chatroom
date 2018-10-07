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
- socket
    - join
    - submit
    - leave

# TODO
0. database
    - remove:UserList
    - modify:Chatroom(change into dict)
    - test for redis roomlist
1. http
    - chatroom operations(update, remove, etc.)
    - ? user operations(update, remove, etc.)
    - upload
    - download
3. upload files
4. message with pictures
5. calendar data

## more
1. use pytest to test each module
2. use click
