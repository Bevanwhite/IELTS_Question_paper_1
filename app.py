from playsound import playsound
from gtts import gTTS
import secrets
import os
from flaskblog import app


print(os.listdir())
print(os.path.split('welcome.mp3'))


def someaudio(form_audio):
    mytext = form_audio
    language = 'en'
    os.chdir('/Users/Bevan/Desktop/New folder (3)/myflaskapp/app')
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


# name = 'i love you so much dulika'
# someaudio(name)


playsound('welcome.mp3')
