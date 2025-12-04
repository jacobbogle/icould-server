import os
import sys
from flask import Flask, Response
from pyicloud import PyiCloudService
from dotenv import load_dotenv

load_dotenv()

apple_id = os.getenv('APPLE_ID')
password = os.getenv('APPLE_PASSWORD')

if not apple_id or not password:
    print("Please set APPLE_ID and APPLE_PASSWORD environment variables.")
    sys.exit(1)

api = PyiCloudService(apple_id, password)

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

def refresh_files():
    global files
    files = {}
    for child in folder.get_children():
        if child.type == 'file' and child.name.lower().endswith(extensions):
            files[child.name] = child

refresh_files()

app = Flask(__name__)

@app.route('/')
def index():
    links = ''.join(f'<a href="/download/{name}">{name}</a><br>' for name in files)
    return f'<html><body><h1>Audio Files in iCloud Drive {directory or "root"}</h1>{links}</body></html>'

@app.route('/download/<filename>')
def download(filename):
    if filename not in files:
        return "File not found", 404
    node = files[filename]
    response = node.open()
    return Response(response.content, mimetype=response.headers.get('Content-Type', 'application/octet-stream'), headers={"Content-Disposition": f"attachment; filename={filename}"})

@app.route('/sync/<path:local_dir>')
def sync(local_dir):
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

if __name__ == '__main__':
    app.run(debug=True)