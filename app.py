from flask import Flask, request
from flask.templating import render_template
from wtforms import Form, StringField, PasswordField, validators

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello"


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    else:
        return render_template('register.html', form=form)
