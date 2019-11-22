from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from registration_form import *
from models import *

#Configuring app
app = Flask(__name__)
app.secret_key = 'replace later'

#configuring database
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://qmatonjvzodehx:32e081e14a510c99955ee0ee9022fa4e7e231d61fb67652e01e4e7d0c4967523@ec2-174-129-214-42.compute-1.amazonaws.com:5432/d4chmbbe0pv6cj'
db = SQLAlchemy(app)


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
    if not current_user.is_authenticated:
        flash('Please login.','danger')
        return redirect(url_for('login'))
    
    return "Chat with me"
    
@app.route("/logout",  methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)