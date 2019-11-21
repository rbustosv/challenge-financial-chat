from flask import Flask, render_template

from form import *
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
        username = user_form.name.data
        password = user_form.password.data

        #validating username
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Username already taken. Please try with a different one"

        #creating user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "User created"


    return render_template("index.html", form=user_form)

if __name__ == "__main__":
    app.run(debug=True)