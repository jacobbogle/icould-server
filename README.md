# Family Media Server with iCloud Integration

A comprehensive Flask-based media server that integrates with iCloud Drive to provide family-shared access to audio files, ebooks, and documents with advanced user management, parental controls, and hierarchical account system.

## 🎵 Features

### Core Functionality
- **iCloud Drive Integration**: Seamlessly access and download media files from iCloud Drive
- **Multi-Format Support**: Audio (MP3, WAV, FLAC, AAC, OGG, M4A), Ebooks (EPUB, PDF), Documents
- **Categorized Content**: Organized tabs for Audiobooks, Music, Ebooks, and Documents
- **Bidirectional Sync**: Sync local files to iCloud and download from iCloud to local

### User Management System
- **Hierarchical Accounts**: Admin, Parent, Single User, Kid, and Teen accounts
- **Role-Based Access**: Different permissions and content restrictions per user type
- **Parental Controls**: Kids and Teens have limited access compared to parents
- **Account Limits**: Maximum 10 family accounts per parent user

### Security & Authentication
- **Secure Login**: Session-based authentication with password hashing
- **Double Password Confirmation**: All password changes and account creation require confirmation
- **Admin Panel**: Complete user management interface for administrators
- **Family Management**: Parents can manage their children's accounts

### Family Features
- **Unified Family Tab**: Combined Kids and Teens management in one interface
- **Account Type Labels**: Clear identification of Kid vs Teen accounts
- **Password Management**: Secure password changes for all account types
- **Account Creation**: Streamlined creation of family member accounts

## 📁 Project Structure

```
iCloud-Server/
├── backend/                          # Python application code
│   ├── app.py                       # Main Flask application
│   ├── auth.py                      # Authentication & user management
│   ├── routes.py                    # Route handlers & business logic
│   ├── icloud_service.py            # iCloud Drive integration
│   ├── config.py                    # Configuration & environment variables
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   ├── users.json                   # User account storage
│   ├── kids.json                    # Kids account storage
│   ├── teens.json                   # Teens account storage
│   └── icloud_credentials.json      # iCloud authentication data
├── frontend/                        # Frontend assets
│   ├── templates/                   # Jinja2 HTML templates
│   │   ├── index.html              # Main application interface
│   │   ├── login.html              # Login page
│   │   └── tabs/                   # Tab-specific templates
│   │       ├── _audiobooks_tab.html
│   │       ├── _music_tab.html
│   │       ├── _ebooks_tab.html
│   │       ├── _documents_tab.html
│   │       ├── _family_tab.html    # Combined kids/teens management
│   │       ├── _settings_tab.html
│   │       ├── _sync_tab.html
│   │       └── _users_tab.html     # Admin user management
│   └── static/                     # CSS, JS, images (if any)
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Apple ID with iCloud Drive access
- Git (for cloning/updating)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/icould-server.git
   cd icould-server
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cd backend
   cp .env.example .env
   ```
   Edit `.env` with your credentials:
   ```env
   APPLE_ID=your_apple_id@example.com
   APPLE_PASSWORD=your_apple_password
   SECRET_KEY=your_random_secret_key_here
   ```

4. **Run the server:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Open http://127.0.0.1:5000 in your browser
   - Default admin login: `admin` / `password`

## 👥 User Types & Permissions

### Administrator
- Full system access
- User account management
- iCloud connection monitoring
- All content tabs access

### Parent Users
- Family account management (create/manage kids & teens)
- Full content access
- Settings and sync capabilities
- Maximum 10 family accounts

### Single Users
- Individual account access
- Full content access
- Personal settings management

### Kids & Teens
- Restricted content access
- No account management capabilities
- Parental supervision required

## 🔧 Configuration

### iCloud Setup
1. Ensure 2FA is enabled on your Apple ID
2. First run may require manual 2FA verification in browser
3. Credentials are securely stored locally

### Environment Variables
- `APPLE_ID`: Your Apple ID email
- `APPLE_PASSWORD`: Your Apple password
- `SECRET_KEY`: Random string for Flask sessions

### Account Management
- Change default admin password immediately
- Create parent accounts for family management
- Set up kids/teens accounts through Family tab
- Use Settings tab for password changes

## 📱 Usage Guide

### For Administrators
1. **Login** with admin credentials
2. **Users Tab**: Create and manage all user accounts
3. **Monitor iCloud Status**: Check connection in header
4. **Content Management**: Access all media categories

### For Parents
1. **Login** with parent account
2. **Family Tab**: Create and manage kids/teens accounts
3. **Content Access**: Full access to all media types
4. **Settings**: Change passwords and preferences

### For Family Members
1. **Login** with individual credentials
2. **Content Access**: Browse and download available media
3. **Limited Features**: No account management access

### Sync Operations
- **Download from iCloud**: Use content tabs to browse and download
- **Upload to iCloud**: Visit `/sync/<local_directory_path>` to sync local files

## 🔒 Security Features

- **Password Hashing**: All passwords securely hashed with SHA-256
- **Session Management**: Secure Flask sessions with secret keys
- **Double Confirmation**: All password operations require confirmation
- **Role-Based Access**: Granular permissions per user type
- **Account Isolation**: Family accounts properly segregated

## 🛠️ Development

### Adding New Features
1. Backend logic in `backend/routes.py`
2. Authentication in `backend/auth.py`
3. Frontend templates in `frontend/templates/`
4. Update this README for documentation

### File Organization
- Keep user data in JSON files within `backend/`
- Static assets in `frontend/static/`
- Templates follow `_component_tab.html` naming

## 📋 Supported File Formats

### Audio Files
- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- AAC (.aac)
- OGG (.ogg)
- M4A (.m4a)

### Ebooks
- EPUB (.epub)
- PDF (.pdf)

### Documents
- All file types supported by iCloud Drive

## ⚠️ Important Notes

- **Security**: Change default passwords immediately
- **iCloud 2FA**: Handle two-factor authentication manually on first run
- **Account Limits**: Maximum 10 family accounts per parent
- **File Sync**: Sync operations are one-way (local → iCloud)
- **Browser Compatibility**: Modern browsers recommended

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please respect copyright and licensing terms.

---

**Built with Flask, pyicloud, and family-friendly design principles.**