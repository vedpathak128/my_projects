import speech_recognition as sr
import webbrowser
from client import ask_groq
import pywhatkit
recognizer = sr.Recognizer()


import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processcomand(c):
    
    if  "open" in c:
        site = c.split("open", 1)[1].strip()
        webbrowser.open(f"https://{site}.com")
    elif "play" in c:
        song = c.split("play", 1)[1].strip()
        pywhatkit.playonyt(song)
    else:
        reply = ask_groq(c)
        print(f"Jarvis: {reply}")
        speak(reply)

if __name__== "__main__":
    speak("Initializing Jarvis, what do you want.....")
    while True:
        r = sr.Recognizer()
        print("recognizing.....")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            command = r.recognize_google(audio)
            if command.lower() == "jarvis":
                speak("yes")
                with sr.Microphone() as source:
                    print("jarvis active....")
                    audio = r.listen(source, timeout=2, phrase_time_limit=3)
                    command = r.recognize_google(audio)
                    processcomand(command)
        except Exception as e:
            print("error: {}".format(e))