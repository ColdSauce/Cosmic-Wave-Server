from flask import Flask, request, send_from_directory
import requests
import twilio
import os
import twilio.twiml
from twilio.rest import TwilioRestClient
import base64
import wave

MAIN_PN = '6504828371'
IP = '127.0.0.1'
PORT = '5000'
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

app = Flask(__name__)

@app.route('/sounds/<path:path>')
def get_file(path):
    return send_from_directory('sounds', path)

@app.route('/playSoundXml', methods=['POST','GET'])
def play_sound_xml():
    resp = twilio.twiml.Response()
    resp.play('http://e4a7d353.ngrok.io/sounds/' + 'something.wav')
    return str(resp)

@app.route('/recordSoundXml', methods=['POST','GET'])
def record_sound_xml():
    resp = twilio.twiml.Response()
    resp.record(maxLength='10', action='/record_callback',trim='do-not-trim')
    return str(resp)

@app.route('/record_callback', methods=['GET','POST'])
def record_callback():
    payload = {'RecordingUrl' : request.values.get('RecordingUrl', None)}
    requests.post(IP + ":" + PORT + "/handle_receive_phone", data=payload)
    return ""
    

@app.route('/recordSound/<int:seconds>', methods=['POST','GET'])
def record_sound(seconds):
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.calls.create(to=MAIN_PN, from_='18559977576',url='http://e4a7d353.ngrok.io/playSoundXml')
    return ""



@app.route('/playSound', methods=['POST','GET'])
def play_sound():
    b_song = request.get.value('audio', None)
    real_song = BytesIO(base64.b64decode(b_song))
    song_name = 'sounds/something.wav'
    with open(song_name, 'w') as soundToPlayFile:
        soundToPlayFile.write(real_song.getvalue())

    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.calls.create(to=MAIN_PN, from_='18559977576',url='http://e4a7d353.ngrok.io/playSoundXml')
    return ""


if __name__ == '__main__':
    app.run(port=6736, debug=True)
