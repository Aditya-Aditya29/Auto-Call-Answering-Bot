import time
import threading
import os
import smtplib
import requests
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from google.cloud import speech
from email.message import EmailMessage
from dotenv import load_dotenv

# Load env vars and Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
load_dotenv()

print("Using Google credentials from:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

app = Flask(__name__)

# Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
EMAIL_USER = os.getenv('GMAIL_USER')
EMAIL_PASS = os.getenv('GMAIL_PASS')
TO_EMAIL = "Where you want all the customer email!!"
PUBLIC_URL = "https://your-ngrok-url.ngrok-free.app"  # Replace every time ngrok restarts

@app.route("/answer", methods=['POST'])
def answer_call():
    response = VoiceResponse()
    gather = Gather(
        input='speech dtmf',
        action=f'{PUBLIC_URL}/process-input',
        method='POST'
    )
    gather.say("Hi I'm Sam, a bot from company Lanka Shop. Today I will assist you. What is your problem today? Press 1 to speak.")
    response.append(gather)
    return Response(str(response), mimetype='text/xml')

@app.route("/process-input", methods=['POST'])
def process_input():
    response = VoiceResponse()
    if 'Digits' in request.form and request.form['Digits'] == '1':
        response.say("After the beep, start speaking. When you're finished, press the pound key to save.")
        response.pause(length=1)
        response.record(
            action=f'{PUBLIC_URL}/thanks',
            method='POST',
            timeout=5,
            maxLength=120,
            finishOnKey='#',
            recordingStatusCallback=f'{PUBLIC_URL}/handle-recording',
            recordingStatusCallbackMethod='POST'
        )
    else:
        response.say("Invalid input. Please call back.")
        response.hangup()
    return Response(str(response), mimetype='text/xml')

@app.route("/thanks", methods=['POST'])
def thanks():
    response = VoiceResponse()
    response.say("Thank you. Your response has been saved. We will contact you shortly.")
    response.hangup()
    return Response(str(response), mimetype='text/xml')

@app.route("/handle-recording", methods=['POST'])
def handle_recording():
    recording_url = request.form.get('RecordingUrl')
    print("🔍 Recording URL:", recording_url)
    if recording_url:
        threading.Thread(target=process_recording, args=(recording_url,)).start()
    return ('', 204)

def process_recording(recording_url):
    try:
        transcript = transcribe_audio(recording_url)
        send_email(transcript)
    except Exception as e:
        print("❌ Error processing recording:", str(e))

def transcribe_audio(audio_url):
    for attempt in range(5):
        time.sleep(2)
        response = requests.get(audio_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        if response.status_code == 200:
            print("✅ Recording downloaded successfully.")
            break
        print(f"❌ Attempt {attempt+1} failed: {response.status_code}. Retrying...")
    else:
        raise Exception("Failed to download audio after retries")

    audio_content = response.content
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=8000,
        language_code="en-US"
    )
    audio = speech.RecognitionAudio(content=audio_content)
    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return "No speech detected"
    return response.results[0].alternatives[0].transcript

def send_email(transcript):
    msg = EmailMessage()
    msg.set_content(f"New Customer Message:\n\n{transcript}")
    msg['Subject'] = 'Customer Complaint from Auto Bot'
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
