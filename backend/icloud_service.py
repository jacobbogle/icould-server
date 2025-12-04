import sys
import os
import json
from pyicloud import PyiCloudService

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'icloud_credentials.json')

api = None
authenticated = False
requires_2fa = False
directory = ''
folder = None
extensions = ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a')
files = {}

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_credentials(apple_id, apple_password):
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump({'apple_id': apple_id, 'apple_password': apple_password}, f)

def authenticate(twofa_code=None):
    global api, authenticated, folder, directory, requires_2fa
    creds = load_credentials()
    apple_id = creds.get('apple_id')
    apple_password = creds.get('apple_password')
    if not apple_id or not apple_password:
        return False
    
    if api is None:
        api = PyiCloudService(apple_id, apple_password)
    
    if api.requires_2fa:
        if twofa_code:
            result = api.validate_2fa_code(twofa_code)
            if result:
                authenticated = True
                requires_2fa = False
            else:
                return False
        else:
            requires_2fa = True
            return '2fa_required'
    else:
        authenticated = True
        requires_2fa = False
    
    if authenticated and folder is None:
        # Use root folder for now
        folder = api.drive.root
        directory = ""
        refresh_files()
    return authenticated

def refresh_files():
    global files
    if not authenticated or folder is None:
        files = {}
        return
    files = {}
    for child in folder.get_children():
        if child.type == 'file' and child.name.lower().endswith(extensions):
            files[child.name] = child