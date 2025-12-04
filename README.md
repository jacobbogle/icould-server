# iCloud Audio Server

A simple Flask server to serve download links for audio files in a given directory.

## Usage

1. Place your audio files in a directory (e.g., `audio` folder or specify path).

2. Run the server:

   ```bash
   python app.py [directory_path]
   ```

   If no directory_path is provided, it defaults to 'audio'.

3. Open http://127.0.0.1:5000/ in your browser to see the list of audio files with download links.

## Supported Formats

- .mp3
- .wav
- .flac
- .aac
- .ogg
- .m4a

## Requirements

- Python 3.x
- Flask (installed via requirements.txt)