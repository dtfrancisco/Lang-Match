from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/browse')
def browse():
    return render_template('browse.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for {form.username.data}, remember me={form.remember_me.data}')
        return redirect(url_for('browse'))
    return render_template('login.html', form=form)
