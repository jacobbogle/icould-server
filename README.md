# iCloud Audio Server

A simple Flask server to serve download links for audio files from an iCloud Drive directory.

## Setup

1. Install dependencies: `pip install -r requirements.txt`

2. Set environment variables for your Apple ID:
   - `APPLE_ID`: Your Apple ID email
   - `APPLE_PASSWORD`: Your Apple ID password

   On Windows PowerShell:
   ```
   $env:APPLE_ID = "your@email.com"
   $env:APPLE_PASSWORD = "yourpassword"
   ```

3. Run the server:
   ```
   python app.py [directory_name]
   ```
   - `directory_name`: Optional subfolder in iCloud Drive root (e.g., "Music"). If omitted, uses root.

4. If 2FA is required, the script will exit. Handle 2FA manually in a browser first.

5. Open http://127.0.0.1:5000/ to view and download audio files.

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