from Flask import flask
from BytesIO import BytesIO
import CosmicWaveModem.cosmicmodem as cosmicmodem
import requests

app = Flask(__name__)

@app.route("/audio", methods=['POST'])
def send_audio_bits():
    resp = twilio.twiml.Response()

@app.route("/receivePhone", methods=['GET', 'POST'])
def receive_phone():
    resp = twilio.twiml.Response()
    resp.record(maxLength="10",action="/handle_receive_phone", trim="do-not-trim")
    return str(resp)

@app.route("/handle_receive_phone", methods=['GET','POST'])
def handle_receive_phone():
    resp = twilio.twiml.Response()
    recording_url = request.values.get("RecordingUrl", None)
    response = requests.get(recording_url)
    audio = ByteIO(response.content)
    get_samples_from_audio(audio)

#def get_frames_from_wav(wav):
    #opened_wav = wave.open(wav)
    #total_frames = opened_wav.getnframes()
    #return bytearray(opened_wav.readframes(total_frames))

""" Gets an array of doubles that is the array of samples """
#def get_url_from_audio(audio_bytes):




