from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from registration_form import *
from models import *

#Configuring app
app = Flask(__name__)
app.secret_key = 'replace later'

#configuring database
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://qmatonjvzodehx:32e081e14a510c99955ee0ee9022fa4e7e231d61fb67652e01e4e7d0c4967523@ec2-174-129-214-42.compute-1.amazonaws.com:5432/d4chmbbe0pv6cj'
db = SQLAlchemy(app)

#Initializing Flask-SocketIO
socketio = SocketIO(app)

#predefined rooms
ROOMS = ["general", "dancers", "readers"]

# configuring flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader

def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET','POST'])

def registration():
    
    user_form = userForm()
    if user_form.validate_on_submit():
        #reading user credentials
        username = user_form.username.data
        password = user_form.password.data

        hashed_psswd = pbkdf2_sha256.hash(password)

        #creating user
        user = User(username=username, password=hashed_psswd)
        db.session.add(user)
        db.session.commit()

        #message to be sent into the login page
        flash('Registered successfully. Please login.','success')

        return redirect(url_for('login'))


    return render_template("index.html", form=user_form)

@app.route("/login", methods=['GET','POST'])

def login(): 

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)   

@app.route("/chat", methods=['GET','POST'])
#@login_required
def chat():
    #if not current_user.is_authenticated:
        #flash('Please login.','danger')
        #return redirect(url_for('login'))
    
    return render_template('chat.html', username=current_user.username,
    rooms=ROOMS)
    
@app.route("/logout",  methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))

@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': 
        strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])

@socketio.on('join')     
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + "has joined the " + data['room'] + "room."}, room=data['room'])

@socketio.on('leave')     
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + "has left the " + data['room'] + "room."}, room=data['room'])



if __name__ == "__main__":
    socketio.run(app, debug=True)