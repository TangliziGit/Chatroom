import json, time, random
import chatroom
from chatroom import config

# ---------- init ----------
app=chatroom.create_app()
socket=chatroom.create_socket(app)

# ---------- socket ----------

# ---------- http ----------
@app.errorhandler(404)
def page_not_find(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
def index():
    if not 'userName' in session:
        return redirect('login')
    return render_template('index.html', user_name=sesseon['userName'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        session['userName']=request.form['userName']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

if __name__=='__main__':
    app.run(config.WEB_ADDR, port=config.WEB_PORT)
