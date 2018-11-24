from flask import (Flask, redirect)

app=Flask(__name__)

@app.route('/index', methods=['GET'])
def index():
    return '<h1>Oops!</h1>\n<h3>Chatroom maybe encounter a knotty bug.</h3>'

@app.route('/', methods=['GET'])
def main():
    return redirect('/index')

app.run('0.0.0.0', port=80)
