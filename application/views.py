from flask.helpers import flash
from .models import db, User
from flask import current_app as app, redirect, url_for

from flask import request
from flask.templating import render_template
from .form import RegistrationForm
from passlib.hash import sha256_crypt


@app.route('/')
def index():
    return "Hello"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form.get('email')
        existing_user = User.query.filter(User.email == email).first()
        if existing_user:
            flash("email already register before", "error")
            return render_template('register.html', form=form)
        user = User(
            name=request.form.get('name'),
            email=email,
            password=sha256_crypt.encrypt(str(form.password.data))
        )
        db.session.add(user)
        db.session.commit()

        flash('You are now registered please confirm your email to login', 'success')
        return redirect(url_for("index"))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        pass
    return render_template("login")
