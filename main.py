import speech_recognition as sr
import gtts
from playsound import playsound
import os
from notion import NotionClient
from datetime import datetime

r = sr.Recognizer()

token = "secret_6TL2xuWwmg3hLw2snHfV4f40f55rCVylimvF06Xn9W0"
database_id = "638c6bdb48374500ab9a84890884f4d6"

client = NotionClient(token, database_id)

ACTIVATION_COMMAND = "hungry"

def get_audio():
    with sr.Microphone() as source:
        print("Say something")
        audio = r.listen(source)
        return audio

def audio_to_text(audio):
    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech recognition couldn't understant the audio")
    except sr.RequestError:
        print("Couldn't request results from API")
    return text

def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = './temp.mp3'
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError:
        print("Couldn't play sound")

if __name__ == "__main__":
    while True:
        a = get_audio()
        command = audio_to_text(a)

        if ACTIVATION_COMMAND in command.lower():
            print("activate")
            play_sound("Yummy")

            note = get_audio()
            note = audio_to_text(note)

            if note:
                play_sound(note)

            now = datetime.now().astimezone().isoformat()
            res = client.create_page(note, now, status="Active")
            if res.status_code == 200:
                play_sound("Stored new item")
