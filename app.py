import os
import sys
from flask import Flask, Response
from pyicloud import PyiCloudService

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

# Get audio files
extensions = ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a')
files = {}
for child in folder.get_children():
    if child.type == 'file' and child.name.lower().endswith(extensions):
        files[child.name] = child

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

if __name__ == '__main__':
    app.run(debug=True)