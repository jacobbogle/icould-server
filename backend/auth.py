from flask import session, redirect, url_for, request, render_template
import os
import json
import hashlib

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
            if not users:
                users = {'admin': hash_password('password')}
                save_users(users)
            return users
    users = {'admin': hash_password('password')}
    save_users(users)
    return users

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_admin_password():
    users = load_users()
    return users.get('admin', 'password')

def set_admin_password(new_password):
    users = load_users()
    users['admin'] = hash_password(new_password)
    save_users(users)

def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

TEENS_FILE = os.path.join(os.path.dirname(__file__), 'teens.json')

def load_teens():
    if os.path.exists(TEENS_FILE):
        with open(TEENS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_teens(teens):
    with open(TEENS_FILE, 'w') as f:
        json.dump(teens, f)

def create_teen(parent_username, teen_username, password):
    kids = load_kids()
    teens = load_teens()
    
    # Check total family accounts limit (10)
    current_kids = len(kids.get(parent_username, {}))
    current_teens = len(teens.get(parent_username, {}))
    if current_kids + current_teens >= 10:
        return False, "Maximum 10 family accounts allowed per parent"
    
    if parent_username not in teens:
        teens[parent_username] = {}
    if teen_username in teens[parent_username]:
        return False, "Teen account already exists"
    teens[parent_username][teen_username] = hash_password(password)
    save_teens(teens)
    return True, "Teen account created successfully"

def delete_teen(parent_username, teen_username):
    teens = load_teens()
    if parent_username in teens and teen_username in teens[parent_username]:
        del teens[parent_username][teen_username]
        save_teens(teens)
        return True
    return False

def get_teens_for_user(username):
    teens = load_teens()
    return list(teens.get(username, {}).keys())

def get_all_users():
    users = load_users()
    kids = load_kids()
    teens = load_teens()
    all_users = dict(users)
    for parent_kids in kids.values():
        all_users.update(parent_kids)
    for parent_teens in teens.values():
        all_users.update(parent_teens)
    return all_users

def get_user_type(username):
    """Determine the type of user: 'admin', 'user', 'kid', or 'teen'"""
    if username == 'admin':
        return 'admin'
    
    users = load_users()
    if username in users:
        return 'user'
    
    kids = load_kids()
    for parent_kids in kids.values():
        if username in parent_kids:
            return 'kid'
    
    teens = load_teens()
    for parent_teens in teens.values():
        if username in parent_teens:
            return 'teen'
    
    return 'unknown'

def login():
    error = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        all_users = get_all_users()
        if username in all_users and all_users[username] == hash_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = True
    return render_template('login.html', error=error)

def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def change_password():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']
        users = load_users()
        if users.get(username) == hash_password(current) and new == confirm:
            users[username] = hash_password(new)
            save_users(users)
            return redirect(url_for('index'))
        else:
            error = "Invalid current password or passwords do not match."
            return render_template('change_password.html', error=error)
    return render_template('change_password.html')

def create_user(username, password, confirm_password=None):
    if confirm_password is not None and password != confirm_password:
        return False, "Passwords do not match"
    users = load_users()
    if username in users:
        return False, "User already exists"
    users[username] = hash_password(password)
    save_users(users)
    return True, "User created successfully"

def delete_user(username):
    users = load_users()
    if username in users and username != 'admin':
        del users[username]
        save_users(users)
        return True
    return False

KIDS_FILE = os.path.join(os.path.dirname(__file__), 'kids.json')

def load_kids():
    if os.path.exists(KIDS_FILE):
        with open(KIDS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_kids(kids):
    with open(KIDS_FILE, 'w') as f:
        json.dump(kids, f)

def create_kid(parent_username, kid_username, password, confirm_password=None):
    if confirm_password is not None and password != confirm_password:
        return False, "Passwords do not match"
    kids = load_kids()
    teens = load_teens()
    
    # Check total family accounts limit (10)
    current_kids = len(kids.get(parent_username, {}))
    current_teens = len(teens.get(parent_username, {}))
    if current_kids + current_teens >= 10:
        return False, "Maximum 10 family accounts allowed per parent"
    
    if parent_username not in kids:
        kids[parent_username] = {}
    if kid_username in kids[parent_username]:
        return False, "Kid account already exists"
    kids[parent_username][kid_username] = hash_password(password)
    save_kids(kids)
    return True, "Kid account created successfully"

def delete_kid(parent_username, kid_username):
    kids = load_kids()
    if parent_username in kids and kid_username in kids[parent_username]:
        del kids[parent_username][kid_username]
        save_kids(kids)
        return True
    return False

def get_kids_for_user(username):
    kids = load_kids()
    return list(kids.get(username, {}).keys())

def create_teen(parent_username, teen_username, password, confirm_password=None):
    if confirm_password is not None and password != confirm_password:
        return False, "Passwords do not match"
    teens = load_teens()
    kids = load_kids()
    
    # Check total family accounts limit (10)
    current_kids = len(kids.get(parent_username, {}))
    current_teens = len(teens.get(parent_username, {}))
    if current_kids + current_teens >= 10:
        return False, "Maximum 10 family accounts allowed per parent"
    
    if parent_username not in teens:
        teens[parent_username] = {}
    if teen_username in teens[parent_username]:
        return False, "Teen account already exists"
    teens[parent_username][teen_username] = hash_password(password)
    save_teens(teens)
    return True, "Teen account created successfully"

def change_kid_password(parent_username, kid_username, new_password, confirm_password):
    if new_password != confirm_password:
        return False, "Passwords do not match"
    kids = load_kids()
    if parent_username in kids and kid_username in kids[parent_username]:
        kids[parent_username][kid_username] = hash_password(new_password)
        save_kids(kids)
        return True, "Kid password changed successfully"
    return False, "Kid not found"

def change_teen_password(parent_username, teen_username, new_password, confirm_password):
    if new_password != confirm_password:
        return False, "Passwords do not match"
    teens = load_teens()
    if parent_username in teens and teen_username in teens[parent_username]:
        teens[parent_username][teen_username] = hash_password(new_password)
        save_teens(teens)
        return True, "Teen password changed successfully"
    return False, "Teen not found"

def change_user_password(admin_username, target_username, new_password, confirm_password):
    """Admin can change any user's password (except admin's own password should be changed via settings)"""
    if admin_username != 'admin':
        return False, "Only admin can change user passwords"
    if new_password != confirm_password:
        return False, "Passwords do not match"
    
    users = load_users()
    if target_username in users and target_username != 'admin':
        users[target_username] = hash_password(new_password)
        save_users(users)
        return True, "User password changed successfully"
    return False, "User not found or cannot change admin password"

def get_organized_users():
    """Return users organized by type: admin, regular users, and their kids/teens"""
    users = load_users()
    kids = load_kids()
    teens = load_teens()
    
    organized = {
        'admin': ['admin'] if 'admin' in users else [],
        'regular_users': [user for user in users.keys() if user != 'admin'],
        'family_accounts': {}
    }
    
    # Add kids and teens for each parent
    for parent in users.keys():
        if parent != 'admin':
            organized['family_accounts'][parent] = {
                'kids': list(kids.get(parent, {}).keys()),
                'teens': list(teens.get(parent, {}).keys())
            }
    
    return organized