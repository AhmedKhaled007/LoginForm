import os
from functools import wraps

from flask import current_app as app, redirect, url_for, session, flash, send_from_directory, request, render_template
from passlib.hash import sha256_crypt
from flask_security import ForgotPasswordForm
from werkzeug.utils import secure_filename

import requests

from .models import db, User
from .form import RegistrationForm


UPLOAD_FOLDER = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "../uploads")

if not os.path.exists(F'{UPLOAD_FOLDER}'):
    os.makedirs(f'{UPLOAD_FOLDER}')

# Allowed extensions for upload task
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Google map api key for calcuate distance
GOOGLE_MAP_API_KEY = os.environ.get('API_KEY')
GOOGLE_API_BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?region=eg&"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# test file uploaded for allowed extension


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # Get browser info
    user_browser_info = {}
    user_browser_info['version'] = request.user_agent.version
    user_browser_info['browser'] = request.user_agent.browser
    user_browser_info['platform'] = request.user_agent.platform
    user_browser_info['language'] = request.user_agent.language

    return render_template("index.html", user_browser_info=user_browser_info)


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form.get('email')
        existing_user = User.query.filter(User.email == email).first()
        if existing_user:
            flash("email already register before", "danger")
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
        email = request.form.get('email')
        password_raw = request.form.get('password')
        user = User.query.filter(User.email == email).first()

        if user:
            if sha256_crypt.verify(password_raw, user.password):
                session['logged_in'] = True
                session['name'] = user.name
                flash('Welcome back', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Wrong password !', 'danger')

        else:
            error = 'can not found email, please register first'
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', "success")
    return redirect(url_for('index'))


@app.route('/profile')
@is_logged_in
def profile():
    return render_template('profile.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('download_file', name=filename))
    else:
        return render_template("upload.html")

# Download uploaded file


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


# Using google map api  to calculate distance
@app.route('/distance', methods=['GET', 'POST'])
def distance_calculator():
    if request.method == 'POST':

        origin = request.form.get('origin')
        destination = request.form.get('destination')

        r = requests.get(GOOGLE_API_BASE_URL + "origins=" + origin +
                         "&destinations=" + destination + "&key=" + GOOGLE_MAP_API_KEY).json()
        app.logger.warning(f"distance = {r}")

        travel_info = {}
        travel_info['distance'] = r["rows"][0]["elements"][0]["distance"]["text"]
        travel_info['destination'] = r["destination_addresses"][0]
        travel_info['origin'] = r["origin_addresses"][0]
        travel_info['time'] = r["rows"][0]["elements"][0]["duration"]["text"]

        return render_template('distance_calculator.html', travel_info=travel_info)

    return render_template('distance_calculator.html')
