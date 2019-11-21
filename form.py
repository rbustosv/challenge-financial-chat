from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User
class userForm(FlaskForm):

    username = StringField('username',
    validators=[InputRequired(message="Userame required"),
    Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    
    password = PasswordField('password',
    validators=[InputRequired(message="Password required"),
    Length(min=4, max=8, message="Password must be between 4 and 8 characters")])
    
    confirm_psswd  = PasswordField('confirm_psswd',
    validators=[InputRequired(message="Password required"),
    EqualTo('password', message="Password must match")])

    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Name already exists. Select a different name")