# IT17158350
from gtts import gTTS
import secrets
import os
import sounddevice as sd
from scipy.io.wavfile import write
import pyaudio
import speech_recognition as sr
import wavio
from flaskblog import app


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

        print(new_name)
        print(file_name)


def record(seconds, file_name):
    count = 0
    fs = 44100  # sample rate

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('data/' + file_name + '.wav', fs, myrecording)
    wavio.write('static/' + file_name + '.wav', myrecording, fs, sampwidth=2)
    count = count+1
