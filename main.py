from flask import Flask, request
from io import BytesIO
import CosmicWaveModem.cosmicmodem as cosmicmodem
import requests
import sys
import twilio 
import os
import twilio.twiml
import random
import wave
import base64
from bs4 import BeautifulSoup

from twilio.rest import TwilioRestClient

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
SECOND_SERVER_IP = '127.0.0.1'
SECOND_SERVER_PORT = '6736'


@app.route("/", methods=['GET','POST'])
def index():
    return conference_call()

@app.route("/audio", methods=['POST'])
def send_audio_bits():
    resp = twilio.twiml.Response()
    encoded_bytes = request.values.get("audioData", None)
    decoded_bytes = base64.b64decode(encoded_bytes)
    with wave.open('file_to_send.wav', 'w') as wav:
        wav.writeframes(decoded_bytes)
    resp.play('file_to_send.wav')
    return str(resp)

def _strip_element(html, element):
    soup = BeautifulSoup(html)
    for javascript in soup(element):
        javascript.extract()
    return soup.encode('UTF-8')

def strip_js(html):
    return _strip_element(html,'script')

def strip_css(html):
    return _strip_element(html,'css')

def strip_images(html):
    return _strip_element(html,'img')

@app.route('/conference_call', methods=['POST','GET'])
def conference_call():
    resp = twilio.twiml.Response()
    resp.dial().conference('theMagicalRoom', beep='false', waitUrl='', startConferenceOnEnter='true')
    return str(resp)

@app.route("/receivePhone", methods=['GET', 'POST'])
def receive_phone():
    resp = twilio.twiml.Response()
    resp.record(maxLength="15",action="/handle_receive_phone", trim="do-not-trim")
    return str(resp)


def handle_bad_url():
    print 'lolzard bad url'

@app.route("/handle_receive_phone", methods=['GET','POST'])
def handle_receive_phone():
    resp = twilio.twiml.Response()
    recording_url = request.values.get("RecordingUrl", None)
    response = requests.get(recording_url)
    audio = BytesIO(response.content)
    decoded_audio = cosmicmodem.decode(audio)
    url = decoded_audio

    try:
        resp = requests.get(url)
    except:
        handle_bad_url()
        return

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url,headers=headers)
    html = response.content
    stripped_html = strip_css(html)
    stripped_html = strip_js(html)
    stripped_html = strip_images(html)
    audio = cosmicmodem.encode(stripped_html)
    

def play_sound(audio):
    b64_audio = base64.b64encode(audio)
    payload = {'audio': b64_audio}
    base_url = SECOND_SERVER_IP + ':' + SECOND_SERVER_PORT
    requests.post(base_url + "/playSound", data=payload)

if __name__ == '__main__':
    app.run(debug=True)
