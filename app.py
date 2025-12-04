from flask import Flask
from config import SECRET_KEY
from auth import login_required, login, logout
from routes import index, download, sync

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/', 'index', login_required(index))
app.add_url_rule('/download/<filename>', 'download', login_required(download))
app.add_url_rule('/sync/<path:local_dir>', 'sync', login_required(sync))

if __name__ == '__main__':
    app.run(debug=True)