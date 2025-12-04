import sys
from pyicloud import PyiCloudService
from config import APPLE_ID, APPLE_PASSWORD

if not APPLE_ID or not APPLE_PASSWORD:
    print("Please set APPLE_ID and APPLE_PASSWORD environment variables.")
    sys.exit(1)

api = PyiCloudService(APPLE_ID, APPLE_PASSWORD)

if api.requires_2fa:
    print("Two-factor authentication required. Please handle manually.")
    sys.exit(1)

directory = sys.argv[1] if len(sys.argv) > 1 else ''

# Get the folder node
if directory:
    try:
        folder = api.drive.root[directory]
    except KeyError:
        print(f"Directory {directory} not found in iCloud Drive root.")
        sys.exit(1)
else:
    folder = api.drive.root

extensions = ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a')
files = {}

def refresh_files():
    global files
    files = {}
    for child in folder.get_children():
        if child.type == 'file' and child.name.lower().endswith(extensions):
            files[child.name] = child

refresh_files()