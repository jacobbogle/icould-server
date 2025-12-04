import os
from flask import Response, render_template, request, session, redirect, url_for
from icloud_service import api, folder, files_audiobooks, files_music, files_ebooks, files_documents, refresh_files, extensions_audiobooks, extensions_music, extensions_ebooks, extensions_documents, directory, authenticate as icloud_authenticate, authenticated as icloud_authenticated, requires_2fa as icloud_requires_2fa, save_credentials, load_credentials, is_registered
from auth import create_user, delete_user, get_users, create_kid, delete_kid, get_kids_for_user

def index():
    username = session.get('username')
    if request.method == 'POST':
        if not username:
            return "Access denied", 403
        action = request.form.get('action')
        if action == 'create':
            if username != 'admin':
                return "Access denied", 403
            username_form = request.form['username']
            password = request.form['password']
            create_user(username_form, password)
        elif action == 'delete':
            if username != 'admin':
                return "Access denied", 403
            username_form = request.form['username']
            delete_user(username_form)
        elif action == 'create_kid':
            kid_username = request.form['kid_username']
            password = request.form['password']
            create_kid(username, kid_username, password)
        elif action == 'delete_kid':
            kid_username = request.form['kid_username']
            delete_kid(username, kid_username)
    users_list = get_users()
    kids_list = get_kids_for_user(username) if username else []
    return render_template('index.html', 
                           audiobooks=list(files_audiobooks.keys()), 
                           music=list(files_music.keys()), 
                           ebooks=list(files_ebooks.keys()), 
                           documents=list(files_documents.keys()), 
                           directory=directory, 
                           username=username, 
                           icloud_authenticated=icloud_authenticated, 
                           is_registered=is_registered(), 
                           users=users_list,
                           kids=kids_list)

def download(filename):
    if filename not in files:
        return "File not found", 404
    node = files[filename]
    response = node.open()
    return Response(response.content, mimetype=response.headers.get('Content-Type', 'application/octet-stream'), headers={"Content-Disposition": f"attachment; filename={filename}"})

def sync(local_dir=None):
    if request.method == 'POST':
        local_dir = request.form.get('local_dir')
    if not local_dir:
        return "Local directory not provided.", 400
    if not os.path.exists(local_dir):
        return f"Local directory {local_dir} does not exist.", 400
    local_files = [f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f)) and f.lower().endswith(extensions)]
    local_set = set(local_files)
    
    # Upload local files
    synced = 0
    for f in local_files:
        local_path = os.path.join(local_dir, f)
        with open(local_path, 'rb') as file_obj:
            api.drive.send_file(folder.data['drivewsid'], file_obj)
        synced += 1
    
    # Delete iCloud files not in local
    deleted = 0
    for name, node in list(files.items()):
        if name not in local_set:
            api.drive.move_items_to_trash(node.data['docwsid'], node.data['etag'])
            deleted += 1
    
    refresh_files()
    return f"Synced {synced} files and deleted {deleted} files. Local: {local_dir} to iCloud Drive {directory or 'root'}."

def icloud_login():
    if session.get('username') != 'admin':
        return "Access denied", 403
    creds = load_credentials()
    has_creds = bool(creds.get('apple_id') and creds.get('apple_password'))
    if request.method == 'POST':
        if 'apple_id' in request.form:
            # Setting credentials
            apple_id = request.form['apple_id']
            apple_password = request.form['apple_password']
            save_credentials(apple_id, apple_password)
            # Try to authenticate
            result = icloud_authenticate()
            if result == '2fa_required':
                return render_template('icloud_login.html', requires_2fa=True, has_creds=True, error=None)
            elif result:
                return redirect(url_for('index'))
            else:
                return render_template('icloud_login.html', has_creds=True, error="Authentication failed")
        else:
            # Submitting 2FA code
            twofa_code = request.form.get('twofa_code')
            result = icloud_authenticate(twofa_code)
            if result:
                return redirect(url_for('index'))
            else:
                return render_template('icloud_login.html', requires_2fa=True, has_creds=True, error="Invalid 2FA code")
    if icloud_authenticated:
        return render_template('icloud_login.html', authenticated=True, has_creds=True)
    elif icloud_requires_2fa:
        return render_template('icloud_login.html', requires_2fa=True, has_creds=True)
    elif has_creds:
        return render_template('icloud_login.html', has_creds=True, retry=True)
    else:
        return render_template('icloud_login.html', has_creds=False)