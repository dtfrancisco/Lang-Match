from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, AnswerForm, SettingsForm
from app.models import User, Question, Answer
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/browse')
@app.route('/browse/')
@login_required
def browse():
    return render_template('browse.html', title='Browse')


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid username or password')
            return redirect(url_for('browse'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if current_user.last_seen:
            # Set next_page to browse if not set and also set it to browse in case external website is provided
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('browse')
        else:
            next_page = url_for('user_preferences')
        return redirect(next_page)
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('browse'))


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Thanks for registering!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/profile')
@app.route('/profile/')
@login_required
def user_profile():
    return redirect(url_for('profile', username=current_user.username))


@app.route('/profile/<username>', methods=['GET', 'POST'])
@app.route('/profile/<username>/', methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    questions = Question.query.filter_by(type='summary').all()
    return render_template('profile.html', user=user, questions=questions, Answer=Answer, title=user.username)


@app.route('/answer/<id>', methods=['GET', 'POST'])
@app.route('/answer/<id>/', methods=['GET', 'POST'])
@login_required
def answer(id):
    # Figure out if answer already exists
    question = Question.query.get(int(id))
    answer = Answer.query.filter_by(author=current_user).filter_by(question=question).first()

    form = AnswerForm()
    # If answer doesn't yet exist
    if answer is None:
        if form.validate_on_submit():
            answer = Answer(body=form.body.data, author=current_user, question=question)
            db.session.add(answer)
            db.session.commit()
            flash(f'Your response has been recorded')
            return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.body.data = answer.body
    # Validate an existing answer
    elif form.validate_on_submit():
        answer.body = form.body.data
        db.session.commit()
        flash(f'Your response has been edited')
        return redirect(url_for('profile', username=current_user.username))
    return render_template('answer.html', form=form, question=question, title='Answer')


@app.route('/settings')
@app.route('/settings/')
@login_required
def settings_menu():
    return render_template('settings_menu.html', title='Settings')


@app.route('/preferences', methods=['GET', 'POST'])
@app.route('/preferences/', methods=['GET', 'POST'])
@login_required
def user_preferences():
    return render_template('user_preferences.html', title='Preferences')


@app.route('/user_settings', methods=['GET', 'POST'])
@app.route('/user_settings/', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = SettingsForm(current_user.email, current_user.username)
    if request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.gender.data = current_user.gender
        form.birthday.data = current_user.birthday
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zip_code.data = current_user.zip_code
        form.privacy.data = current_user.privacy
    elif form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.gender = form.gender.data
        current_user.birthday = form.birthday.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zip_code = form.zip_code.data
        current_user.privacy = form.privacy.data
        db.session.commit()
        flash(f'Your settings have been updated')
        return redirect(url_for('user_settings'))
    return render_template('user_settings.html', form=form, title='User Settings')
