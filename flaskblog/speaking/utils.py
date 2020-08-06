# IT17158350
from gtts import gTTS
import secrets
import os
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
import pyaudio
import speech_recognition as sr
import wavio
from flaskblog import app
import numpy as np


def Someaudio(form_audio):
    mytext = form_audio
    language = 'en'
    os.chdir('/Users/Bevan/Desktop/New folder (3)/myflaskapp/flaskblog/static/audio')
    print(os.listdir())
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save('welcome.mp3')

    for f in os.listdir():
        file_name, file_ext = os.path.splitext(f)
        random_hex = secrets.token_hex(8)
        new_name = '{}{}'.format(random_hex, file_ext)
        if(file_name == 'welcome'):
            os.rename(f, new_name)
            return new_name


count = 0


def record(seconds):
    global count
    fs = 44100  # sample rate
    random_file_name = secrets.token_hex(8)
    myrecoding = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
    sd.wait()
    os.chdir('/Users/Bevan/Desktop/New folder (3)/myflaskapp/flaskblog/static/')
    wavio.write('data/' + random_file_name +
                '.wav', myrecoding, fs, sampwidth=2)
    count = count+1
    r = sr.Recognizer()
    os.chdir('/Users/Bevan/Desktop/New folder (3)/myflaskapp/flaskblog/static/')
    file = sr.AudioFile('data/' + random_file_name + '.wav')

    with file as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='en')
        print(text)
        marks = text
    except sr.UnknownValueError:
        marks = 'none'
        os.chdir(
            '/Users/Bevan/Desktop/New folder (3)/myflaskapp/flaskblog/static/data/')
        os.remove(random_file_name + '.wav')
    return marks
