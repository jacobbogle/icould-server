from flask import Flask
from config import SECRET_KEY
from auth import login_required, login, logout, change_password
from routes import index, download, sync, icloud_login

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = SECRET_KEY

app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/change_password', 'change_password', change_password, methods=['GET', 'POST'])
app.add_url_rule('/icloud_login', 'icloud_login', login_required(icloud_login), methods=['GET', 'POST'])
app.add_url_rule('/', 'index', login_required(index), methods=['GET', 'POST'])
app.add_url_rule('/download/<filename>', 'download', login_required(download))
app.add_url_rule('/sync/<path:local_dir>', 'sync', login_required(sync))
app.add_url_rule('/sync', 'sync_post', login_required(sync), methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)