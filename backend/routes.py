import os
from flask import Response, render_template, request, session, redirect, url_for
from icloud_service import api, folder, files_audiobooks, files_music, files_ebooks, files_documents, refresh_files, extensions_audiobooks, extensions_music, extensions_ebooks, extensions_documents, directory, authenticate as icloud_authenticate, authenticated as icloud_authenticated, requires_2fa as icloud_requires_2fa, save_credentials, load_credentials, is_registered
from auth import create_user, delete_user, get_all_users, create_kid, delete_kid, get_kids_for_user, create_teen, delete_teen, get_teens_for_user, get_user_type, change_kid_password, change_teen_password, change_user_password, get_organized_users

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
            
            is_child = request.form.get('is_child') == 'true'
            is_parent = request.form.get('is_parent') == 'true'
            is_single = request.form.get('is_single') == 'true'
            
            if is_child:
                parent_username = request.form['parent_username']
                is_kid = request.form.get('is_kid') == 'true'
                is_teen = request.form.get('is_teen') == 'true'
                confirm_password = request.form.get('confirm_password')
                
                if is_kid:
                    success, message = create_kid(parent_username, username_form, password, confirm_password)
                elif is_teen:
                    success, message = create_teen(parent_username, username_form, password, confirm_password)
                else:
                    success, message = False, "Must specify if child is kid or teen"
            else:
                # Create regular user (parent or single)
                confirm_password = request.form.get('confirm_password')
                success, message = create_user(username_form, password, confirm_password)
        elif action == 'delete':
            if username != 'admin':
                return "Access denied", 403
            username_form = request.form['username']
            delete_user(username_form)
        elif action == 'create_kid':
            kid_username = request.form['kid_username']
            password = request.form['password']
            confirm_password = request.form.get('confirm_password')
            success, message = create_kid(username, kid_username, password, confirm_password)
            # For now, just proceed - error handling could be added later with flash messages
        elif action == 'delete_kid':
            kid_username = request.form['kid_username']
            delete_kid(username, kid_username)
        elif action == 'create_teen':
            teen_username = request.form['teen_username']
            password = request.form['password']
            confirm_password = request.form.get('confirm_password')
            success, message = create_teen(username, teen_username, password, confirm_password)
            # For now, just proceed - error handling could be added later with flash messages
        elif action == 'create_family_account':
            family_username = request.form['family_username']
            password = request.form['password']
            confirm_password = request.form.get('confirm_password')
            is_kid = request.form.get('is_kid') == 'true'
            is_teen = request.form.get('is_teen') == 'true'
            
            if is_kid:
                success, message = create_kid(username, family_username, password, confirm_password)
            elif is_teen:
                success, message = create_teen(username, family_username, password, confirm_password)
            else:
                success, message = False, "Must specify if account is for Kid or Teen"
            # For now, just proceed - error handling could be added later with flash messages
        elif action == 'delete_teen':
            teen_username = request.form['teen_username']
            delete_teen(username, teen_username)
        elif action == 'change_kid_password':
            kid_username = request.form['kid_username']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            success, message = change_kid_password(username, kid_username, new_password, confirm_password)
        elif action == 'change_teen_password':
            teen_username = request.form['teen_username']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            success, message = change_teen_password(username, teen_username, new_password, confirm_password)
        elif action == 'change_user_password':
            target_username = request.form['target_username']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            success, message = change_user_password(username, target_username, new_password, confirm_password)
    users_list = get_all_users()
    kids_list = get_kids_for_user(username) if username else []
    teens_list = get_teens_for_user(username) if username else []
    user_type = get_user_type(username) if username else 'unknown'
    organized_users = get_organized_users()
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
                           organized_users=organized_users,
                           kids=kids_list,
                           teens=teens_list,
                           user_type=user_type)

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