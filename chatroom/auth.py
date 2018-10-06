import functools

from flask import (
    Blueprint, session, g, request, render_template, redirect,
    url_for, flash
)

import chatroom
from chatroom import config
from chatroom import utils
from chatroom.database import *

bp=Blueprint('auth', __name__, url_prefix='/auth')

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
                'userId': utils.get_user_id(),
                'userName': userName,
                'userProfile': 'None'
            })
            user_db.insert(user, utils.get_encrypt_password(password))
            session['userId']=user['userId']
            return redirect(url_for('index'))
        else:
            flash(error)
            return render_template('register.html')
    else:
        return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
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
        }) is None:
            error='User `%s` is not registered.'%userName

        user=None
        if error is None:
            user, true_password=user_db.find_one_with_password({
                'userName': userName
            })
            if not utils.check_password(password, true_password):
                error='Incorrect password.'

        if error is None:
            # clear session first like logout
            session.clear()
            # only restore user_id
            session['userId']=user['userId']
            return redirect(url_for('index'))
        else:
            flash(error)
            return render_template('login.html')
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
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in firstly.')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
