import google
from mail import  main as mail 
from wiki import main as wiki
import speech_recognition as sr
import tts, stt, threading, sys, tty, termios
from selenium import webdriver
from pyttsx3 import engine
from sys import exit

class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                print( "up")
        elif k=='\x1b[B':
                print("down")
        elif k=='\x1b[C':
                print("right")
        elif k=='\x1b[D':
                print("left  "+ str(k))
                tts.engine.stop()
                tts.engine.disconnect()
                from main import main_loop
                main_loop()
                # (google.main.driver or wiki.driver or mail.driver).execute_script("window.history.go(-1)")
        else:
                print("not an arrow key!")

def get_t():
    while(True):
        get()

def main_loop():
    threading.Thread(target=get_t).start()
    
    while(True):
        device_id, sample_rate, chunk_size, r = stt.setup()

        with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                        chunk_size = chunk_size) as source:
            r.adjust_for_ambient_noise(source)
            tts.play_plain_text("Hello, What do you want to Do ? Search on Google ?   Search on wikipedia ?   Send a mail ? ")
            text = stt.listen(device_id, sample_rate, chunk_size, r, None, source)
            text = text.lower()
            text = text.strip()

        print(text)
        if "google" in text:
            google.main.run()
        elif "stop" in text or "exit" in text :
            exit(0)
            break
        elif "mail" in text or "gmail" in text:
            mail.run()
        elif "wiki" in text or "wikipedia" in text:
            wiki.run()
        
if __name__ == "__main__":

    main_loop()
