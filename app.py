import threading
import time
from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
from pydub import AudioSegment
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
""""
# Function to remove old files (older than 5 minutes)
def remove_old_files():
    while True:
        current_time = time.time()
        for filename in os.listdir(DOWNLOAD_FOLDER):
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > 300:  # 300 seconds = 5 minutes
                    os.remove(file_path)
                    print(f"Removed old file: {filename}")
        time.sleep(60)  # Check every minute

# Start the background thread for removing old files
threading.Thread(target=remove_old_files, daemon=True).start()
"""
@app.route('/')
def home():
    return "App is running!"

@app.route('/audio', methods=['GET'])
def download_audio():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            output_filename = secure_filename(f"{uuid.uuid4()}.mp3")
            output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)

            # Convert to MP3 using pydub
            audio = AudioSegment.from_file(file_path)
            audio.export(output_path, format="mp3", bitrate="192k")

            # Clean up temporary files
            if os.path.exists(file_path):
                os.remove(file_path)

        return jsonify({'download_url': f'https://getsongragnork.serveo.net/download/{output_filename}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(host='0.0.0.0')
