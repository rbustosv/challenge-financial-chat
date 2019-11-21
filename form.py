from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class userForm(FlaskForm):

    name = StringField('name',
    validators=[InputRequired(message="Name required"),
    Length(min=4, max=25, message="Name must be between 4 and 25 characters")])
    
    password = PasswordField('password',
    validators=[InputRequired(message="Password required"),
    Length(min=4, max=8, message="Password must be between 4 and 8 characters")])
    
    confirm_psswd  = PasswordField('confirm_psswd',
    validators=[InputRequired(message="Password required"),
    EqualTo('password', message="Password must match")])

    submit_button = SubmitField('Create')