from flask import Flask, request, send_file
from flask_cors import CORS
from gtts import gTTS
import os

app = Flask(__name__)
CORS(app)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')
    tts = gTTS(text)
    filename = "output.mp3"
    tts.save(filename)
    return send_file(filename, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
