from flask import session, redirect, url_for, request, render_template

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
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = True
    return render_template('login.html', error=error)

def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))