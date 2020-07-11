import speech_recognition as sr 
import tts
from playsound import playsound
from tab import open_tab
import time
from pyttsx3 import engine

def setup():
    mic_name = "MacBook Pro Microphone"
    #mic = sr.Microphone(device_index=1)
    
    #Sample rate is how often values are recorded 
    sample_rate = 48000
    chunk_size = 2048
    r = sr.Recognizer() 
    
    mic_list = sr.Microphone.list_microphone_names() 
    
    #the following loop aims to set the device ID of the mic that 
    #we specifically want to use to avoid ambiguity. 
    for i, microphone_name in enumerate(mic_list): 
        if microphone_name == mic_name:
            #print(i) 
            device_id = i 
            
    return 0 , sample_rate, chunk_size, r

#function for the mic to listen
def listen(device_id, sample_rate, chunk_size, r, driver, source, flag=False):
     
    # r.adjust_for_ambient_noise(source)    
    r.pause_threshold = 0.8
    print("say your sentence after the beep")
    time.sleep(1.2)
    playsound('beep.wav')
    #listens for the user's input 
    text = ""
    try:
        audio = r.listen(source) 
        text = r.recognize_google(audio)
    #error occurs when google could not understand what was said 
    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand audio") 
    
    except sr.RequestError as e: 
        print("Could not request results from Google")
    
    if "back" in text:
        if driver:
            tts.engine.stop()
            # driver.execute_script("window.history.go(-1)")   
            tts.engine.disconnect()
            from main import main_loop
            main_loop()

    print("Interpreted as %s"%text)
    return text

def speak(text):
    if text != "":
        tts.play_text(text)
    else:
        tts.error_conditon()
