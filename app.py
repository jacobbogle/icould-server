import os
import sys
from flask import Flask, send_from_directory

if len(sys.argv) > 1:
    audio_dir = sys.argv[1]
else:
    audio_dir = 'audio'

app = Flask(__name__)

@app.route('/')
def index():
    if not os.path.exists(audio_dir):
        return f'<html><body>Directory {audio_dir} does not exist.</body></html>'
    files = [f for f in os.listdir(audio_dir) if f.lower().endswith(('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'))]
    links = ''.join(f'<a href="/download/{f}">{f}</a><br>' for f in files)
    return f'<html><body><h1>Audio Files in {audio_dir}</h1>{links}</body></html>'

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(audio_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)