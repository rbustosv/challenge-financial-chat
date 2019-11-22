from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User

def invalid_credentials(form, field):
#custom function validator (external) reusable
    username_entered = form.username.data
    password_entered = field.data #function called from paswd field

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")



class userForm(FlaskForm):
    #User Registration 
    username = StringField('username',
    validators=[InputRequired(message="Username required"),
    Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    
    password = PasswordField('password',
    validators=[InputRequired(message="Password required"),
    Length(min=4, max=8, message="Password must be between 4 and 8 characters")])
    
    confirm_psswd  = PasswordField('confirm_psswd',
    validators=[InputRequired(message="Password required"),
    EqualTo('password', message="Password must match")])

    submit_button = SubmitField('Create')

    #Inline validator
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Name already exists. Select a different name")


class LoginForm(FlaskForm):
    
    username = StringField('username_label',
    validators=[InputRequired(message="Username required")])

    password = PasswordField('password_label',
    validators=[InputRequired(message="Password required"), invalid_credentials])

    submit_button = SubmitField('Login')