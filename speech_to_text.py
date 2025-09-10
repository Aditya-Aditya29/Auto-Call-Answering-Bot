from google.cloud import speech
import requests

def convert_audio_to_text(audio_url):
    audio_content = requests.get(audio_url).content

    client = speech.SpeechClient.from_service_account_file("credentials.json")

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()
