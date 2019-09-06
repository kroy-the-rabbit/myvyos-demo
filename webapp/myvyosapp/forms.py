from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, HiddenField, SelectField
from wtforms.validators import Required, DataRequired, Length, Optional, Email, length, DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username:' , validators=[Required(), Length(4, 24)])
    password = PasswordField('Password', validators=[Required(message="Please enter your password.")])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username:' , validators=[Required(), Length(4, 24)])
    password = PasswordField('Password', validators=[Required(message="Please enter a password."),EqualTo('confirm', message='Password must match confirmation')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign up')

class GenerateApiKeyForm(FlaskForm):
    generate = SubmitField('Generate API Key')

class DeleteApiKeyForm(FlaskForm):
    delete = SubmitField('Delete this API Key')


class SetTrackForm(FlaskForm):
    system_id = HiddenField(validators=[Required()])
    track_id = SelectField("",validators=[Required()])
