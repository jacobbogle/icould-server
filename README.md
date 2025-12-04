# iCloud Audio Server

A simple Flask server to serve download links for audio files from an iCloud Drive directory and sync local audio files to iCloud.

## Setup

1. Install dependencies: `pip install -r requirements.txt`

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Apple ID credentials and a secret key in `.env`:
     ```
     APPLE_ID=your_apple_id@example.com
     APPLE_PASSWORD=your_apple_password
     SECRET_KEY=your_secret_key_here
     ```

3. Run the server:
   ```
   python app.py [directory_name]
   ```
   - `directory_name`: Optional subfolder in iCloud Drive root (e.g., "Music"). If omitted, uses root.

4. If 2FA is required, the script will exit. Handle 2FA manually in a browser first.

5. Open http://127.0.0.1:5000/ to view and download audio files.

## Features

- **Authentication**: Login required. Default username: `admin`, password: `password`. Change in code for security.
- **List and Download**: View audio files in the iCloud directory and download them.
- **Sync Local to iCloud**: Visit `http://127.0.0.1:5000/sync/<local_directory_path>` to sync all audio files from a local directory to the iCloud folder. Uploads new/changed files and deletes iCloud files not present locally.

## Supported Formats

- .mp3
- .wav
- .flac
- .aac
- .ogg
- .m4a

## Requirements

- Python 3.x
- Flask
- pyicloud

## Security Note

Credentials are stored in environment variables. For production, use secure methods.