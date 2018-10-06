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

bp=Blueprint('user', __name__, url_prefix='/user')

@bp.route('/detail', methods=['GET'])
def detail():
    userId=request.args.get('userId', None)

    user=UserDatabase().find_one({
        'userId': userId
    })
    error=None

    if user is None:
        error='User id `%s` not found.'%userId

    if error is None:
        return render_template('userdetail.html', user=user)
    else:
        flash(error)
        return render_template('error.html')

@bp.route('/update', methods=['POST'])
@login_required
def update():
    userName=request.form['userName']
    userProfile=request.form['userProfile']
    originPassword=request.form['originPassword']
    newPassword=request.form['newPassword']

    user_db=UserDatabase()
    user, password=user_db.find_one_with_password({
        'userId': g.user['userId']
    })
    error=None

    if not utils.check_password(originPassword, password):
        error='Original Password is wrong.'
    elif userName is None:
        error='Username is required.'
    elif originPassword is None:
        error='Original Password is required.'

    if error is None:
        new_user=User({
            'userId': g.user['userId'],
            'userName': userName,
            'userProfile': userProfile
        })
        user_db.insert(new_user, utils.get_encrypt_password(newPassword))
        return 'Update successfully.'
    else:
        return error
