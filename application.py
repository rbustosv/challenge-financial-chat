from flask import Flask, render_template, redirect, url_for

from registration_form import *
from models import *

#Configuring app
app = Flask(__name__)
app.secret_key = 'replace later'

#configuring database
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://qmatonjvzodehx:32e081e14a510c99955ee0ee9022fa4e7e231d61fb67652e01e4e7d0c4967523@ec2-174-129-214-42.compute-1.amazonaws.com:5432/d4chmbbe0pv6cj'
db = SQLAlchemy(app)

@app.route("/", methods=['GET','POST'])

def registration():
    
    user_form = userForm()
    if user_form.validate_on_submit():
        #reading user credentials
        username = user_form.username.data
        password = user_form.password.data

        #creating user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template("index.html", form=user_form)

@app.route("/login", methods=['GET','POST'])

def login(): 

    login_form = LoginForm()

    if login_form.validate_on_submit():
        return "Logged in!"

    return render_template("login.html", form=login_form)   

if __name__ == "__main__":
    app.run(debug=True)