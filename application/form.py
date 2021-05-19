
from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField('Name', validators=[
                       validators.InputRequired(),
                       validators.Length(min=3, max=64)
                       ])
    email = StringField('Email', validators=[
                        validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', 'Password do not match')
    ])
    confirm = PasswordField('Confirm Password')
