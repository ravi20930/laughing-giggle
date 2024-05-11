import os
from flask import Flask, request, jsonify
from pydub import AudioSegment
import io
import speech_recognition as sr

app = Flask(__name__)

# Route to serve the frontend HTML file
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Route to handle audio blob and perform speech recognition
@app.route('/recognize', methods=['POST'])
def recognize():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio blob found'}), 400

    audio_blob = request.files['audio']
    
    # Convert blob to WAV format
    try:
        audio_data = AudioSegment.from_file(io.BytesIO(audio_blob.read()))
        wav_data = io.BytesIO()
        audio_data.export(wav_data, format='wav')
        wav_data.seek(0)
    except Exception as e:
        return jsonify({'error': f'Error converting blob to WAV: {str(e)}'}), 500
    
    # Perform speech recognition
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_data) as source:
            audio_data = recognizer.record(source)
        
        transcription = recognizer.recognize_google(audio_data)
        return jsonify({'transcription': transcription})
    except Exception as e:
        return jsonify({'error': f'Error recognizing speech: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
