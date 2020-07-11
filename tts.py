import pyttsx3 

# initialisation
engine = pyttsx3.init()
engine.setProperty('rate',150)

voices = engine.getProperty('voices')
for voice in voices:
    if voice.languages[0]==u'en_IN':
        engine.setProperty('voice',voice.id)
        break


def play_text(text):
# testing
    engine.say("You said:")
    engine.say(text)
    engine.runAndWait()

def error_conditon():
    engine.say("Error: No input")

def play_plain_text(text):
    engine.say(text)
    engine.runAndWait()