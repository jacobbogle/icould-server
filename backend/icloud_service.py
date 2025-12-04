import sys
from pyicloud import PyiCloudService
from config import APPLE_ID, APPLE_PASSWORD

api = None
authenticated = False
requires_2fa = False
directory = ''
folder = None
extensions = ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a')
files = {}

def authenticate(twofa_code=None):
    global api, authenticated, folder, directory, requires_2fa
    if api is None:
        if not APPLE_ID or not APPLE_PASSWORD:
            return False
        api = PyiCloudService(APPLE_ID, APPLE_PASSWORD)
    
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
        # Set directory from config or default
        directory = ''  # or from env
        if directory:
            try:
                folder = api.drive.root[directory]
            except KeyError:
                return False
        else:
            folder = api.drive.root
        refresh_files()
    return authenticated

# Try to authenticate without 2FA first
if APPLE_ID and APPLE_PASSWORD:
    authenticate()

def refresh_files():
    global files
    if not authenticated or folder is None:
        files = {}
        return
    files = {}
    for child in folder.get_children():
        if child.type == 'file' and child.name.lower().endswith(extensions):
            files[child.name] = child