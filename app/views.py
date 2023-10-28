from flask import render_template, redirect, url_for, flash , abort, session
from app import app, db, recaptcha
from app.models import User
from app.forms import RegistrationForm, LoginForm
from io import BytesIO
import pyqrcode
from datetime import datetime, timedelta, timezone


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET','POST'])
def register() :
    form = RegistrationForm()
    if form.validate_on_submit():
        if recaptcha.verify():
            user = User(
                username = form.username.data,
                email = form.email.data,
                password = form.password.data
            )
            try:
                db.session.add(user)
                db.session.commit()           
                flash(f'Account created for {form.username.data}! ', category='success')
                session['username'] = form.username.data
                return redirect(url_for('qr'))
            except:
                db.session.flush()
                db.session.rollback()
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    failed_attempts_key = f"failed_login_attempts_{form.email.data}"
    last_failed_time_key = f"last_failed_login_time_{form.email.data}"

    current_attempts = session.get(failed_attempts_key, 0)
    last_failed_time = session.get(last_failed_time_key, None)

    if last_failed_time and (datetime.now(timezone.utc) - last_failed_time > timedelta(hours=1)):
            session.pop(failed_attempts_key, None)
            session.pop(last_failed_time_key, None)
    
    if current_attempts >= 5:
            time_to_unlock = last_failed_time + timedelta(hours=1) - datetime.now(timezone.utc)
            flash(f'You have exceeded the limit of failed attempts. Please try again in {time_to_unlock}', category='warning')
            return redirect(url_for('login'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.verify_password(form.password.data) and user.verify_totp(form.token.data):
                session.pop(failed_attempts_key, None)
                session.pop(last_failed_time_key, None)
                return redirect(url_for("home"))
            else:
                session[failed_attempts_key] = current_attempts + 1
                session[last_failed_time_key] = datetime.now(timezone.utc)
                flash('Login unsuccessful. Please check your email and password.', category='warning')
        else:
            flash('User not found. Please register.', category='warning')
            return redirect(url_for('register')) 

    return render_template('login.html', form=form)

@app.route('/qr')
def qr():
    if 'username' not in session:
        return redirect(url_for('register'))
    username = session['username']
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('register'))
    return render_template('qr.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

@app.route('/qr_code')
def qr_code():
    if 'username' not in session:
        return redirect(url_for('register'))
    username = session['username']
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    
    del session['username']

    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}



if __name__ == '__main__': 
    app.run(debug=True)