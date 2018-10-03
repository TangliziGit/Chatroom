import functools

from flask import (
    Blueprint, session, g, request, render_template, redirect,
    url_for
)

import chatroom
from chatroom import config
from chatroom import util
from chatroom.database import *

# ---------- init ----------
# app=chatroom.create_app()
# socket=chatroom.create_socket(app)
# user_db=UserDatabase()
# msg_db=MsgDatabase()
bp=Blueprint('auth', __name__, url_prefix='/auth')

# ---------- socket ----------

# ---------- http ----------
# @bp.route('/', methods=['GET'])
# def root():
#     return redirect(url_for('index'))
# 
# @bp.route('/index', methods=['GET'])
# def index():
#     if 'user' not in session:
#         return redirect('login')
#     return render_template('index.html', username=sesseon['userName'])

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        userName=request.form['userName']
        password=request.form['password']
        user_db=UserDatabase()
        error=None

        if userName is None:
            error='Username is required.'
        elif password is None:
            error='Password is required.'
        elif user_db.find_one({
            'userName': userName
        }) is not None:
            error='User `%s` is already registered.'%userName

        if error is None:
            user=User({
                'userId': util.get_user_id(),
                'userName': userName,
                'profile': 'None'
            })
            user_db.insert(user, util.get_encrypt_password(password))
            session['user']=user
            return redirect(url_for('auth.login'))
        else:
            # flash(error)
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        userName=request.form['userName']
        print(type(userName))
        password=request.form['password']
        user_db=UserDatabase()
        error=None

        if userName is None:
            error='Username is required.'
        elif password is None:
            error='Password is required.'
        elif user_db.find_one({
            'userName': userName
        }) is None:
            error='User `%s` is not registered.'%userName

        user=None
        if error is None:
            user, true_password=user_db.find_one_with_password({
                'userName': userName
            })
            if not util.check_password(password, true_password):
                error='Incorrect password.'

        if error is None:
            # clear session first like logout
            session.clear()
            # only restore user_id
            session['userId']=user['userId']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# a good way for each request with auth
@bp.before_app_request
def login_auto():
    userId=session.get('userId', None)

    if userId is None:
        g.user=None
    else:
        g.user=UserDatabase().find_one({
            'userId': userId
        })

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwagrs):
        if 'user' not in g:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
