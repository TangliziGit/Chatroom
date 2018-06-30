# TODO:
# 1. deal with secure problems
# 2. maybe more beautiful?

import json, time, random

from flask import *
from pymongo import MongoClient

import config

app=Flask(__name__)
app.config.from_object(config)

mcol=MongoClient().ChatRoom.messages
idset=set([])

def get_time():
    return round(time.time()*1000)

def get_random_id():
    rand_value=random.randint(1, 9999)
    while rand_value in idset:
        rand_value=random.randint(1, 9999)
    idset.add(rand_value)
    return ("%s"%(rand_value)).zfill(4)

@app.errorhandler(404)
def page_not_find(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def index():
    if session.get('user_id', None):
        return render_template('index.html', user_name=session['user_name'])
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id', None):
        return redirect('/')
    if request.method=='POST':
        username=request.form['userName']
        if not username:
            return render_template('login.html', info="not entered user name.")
        else:
            session['user_id']=get_random_id()
            session['user_name']=escape(username)
            session['last_submit_time']=get_time()
            return redirect('/')
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    user_id=session.get('user_id', '')
    if user_id in idset:
        idset.remove(user_id)
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('last_submit_time', None)
    return redirect('/login')

@app.route('/post', methods=['POST'])
def get_message():
    form=request.form
    if not session.get("user_id", None):
        return redirect('/login')
    if 'content' in form:
        session['last_submit_time']=get_time()
        msg={"time":int(session['last_submit_time']),
             "user_id":session['user_id'],
             "user_name":session['user_name'],
             "content":escape(form['content'])}
        mcol.insert(msg)
        return "Succeed."
    return "Failed."

@app.route('/get', methods=['GET'])
def find_messages():
    # print(session.get('user_id', 'None'), session['user_name'])
    if session.get("user_id", None):
        res=list(mcol.find({'time':{'$gte': session['last_submit_time']},
                            'user_id':{'$ne': session['user_id']}}, {'_id':0}))
        session['last_submit_time']=get_time()
        return json.dumps(res)
    return "[]"

if __name__=='__main__':
    app.run()
