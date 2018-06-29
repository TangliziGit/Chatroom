# TODO:
# 1. use session
# 2. use uniqe user_id instead of userName
# 3. deal with secure problems
# 4. maybe more beautiful?

import json

from flask import *
from pymongo import MongoClient

app=Flask(__name__)
mcol=MongoClient().ChatRoom.messages

@app.errorhandler(404)
def page_not_find(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def get_message():
    form=request.form
    if 'time' in form and 'user' in form and 'content' in form:
        # secure problems!!!!!!!
        msg={"time":int(form['time']), "user":form['user'],
                'content':form['content']}
        mcol.insert(msg)
        return "Succeed."
    return "Failed."

@app.route('/get', methods=['GET'])
def find_messages():
    time=request.args.get('time', None)
    user=request.args.get('user', None)
    if time and user:
        res=list(mcol.find({'time':{'$gt': int(time)},
                            'user':{'$ne': user}}, {'_id':0}))
        return json.dumps(res)
    else:
        return None

if __name__=='__main__':
    app.run()
