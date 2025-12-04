import os
from flask import Response, render_template, request, session
from icloud_service import api, folder, files, refresh_files, extensions, directory
from auth import create_user, delete_user, get_users

def index():
    return render_template('index.html', files=list(files.keys()), directory=directory, username=session.get('username'))

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

def users():
    if session.get('username') != 'admin':
        return "Access denied", 403
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            username = request.form['username']
            password = request.form['password']
            if not create_user(username, password):
                return "User already exists", 400
        elif action == 'delete':
            username = request.form['username']
            if not delete_user(username):
                return "Cannot delete user", 400
    users_list = get_users()
    return render_template('tabs/_users_tab.html', users=users_list)