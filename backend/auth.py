from flask import session, redirect, url_for, request, render_template
import os

ADMIN_PASSWORD_FILE = os.path.join(os.path.dirname(__file__), 'admin_password.txt')

def get_admin_password():
    if os.path.exists(ADMIN_PASSWORD_FILE):
        with open(ADMIN_PASSWORD_FILE, 'r') as f:
            return f.read().strip()
    return 'password'

def set_admin_password(new_password):
    with open(ADMIN_PASSWORD_FILE, 'w') as f:
        f.write(new_password)

def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def login():
    error = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == get_admin_password():
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = True
    return render_template('login.html', error=error)

def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def change_password():
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']
        if current == get_admin_password() and new == confirm:
            set_admin_password(new)
            return redirect(url_for('index'))
        else:
            error = "Invalid current password or passwords do not match."
            return render_template('change_password.html', error=error)
    return render_template('change_password.html')