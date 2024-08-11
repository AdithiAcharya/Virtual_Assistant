from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pyttsx3 as p
import requests
import randfacts
from news import *
from weather import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize pyttsx3 engine globally
engine = p.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Create a lock for thread safety
engine_lock = threading.Lock()

def speak(text):
    # Run pyttsx3 in a separate thread to avoid blocking
    def run_speech():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()

    threading.Thread(target=run_speech).start()

class Music:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def play(self, query):
        self.query = query
        self.driver.get("https://www.youtube.com/results?search_query=" + query)
        time.sleep(3)
        videos = self.driver.find_element(By.XPATH, '//*[@id="dismissible"]/div')
        videos.click()

class Infow:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def get_info(self, query):
        self.query = query
        try:
            self.driver.get("https://www.wikipedia.org")
            search = self.driver.find_element(By.XPATH, '//input[@id="searchInput"]')
            search.click()
            search.send_keys(query)
            enter = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            enter.click()
        except Exception as e:
            print(f"An error occurred: {e}")

    def __del__(self):
        self.driver.quit()

def joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    json_data = requests.get(url).json()
    return [json_data["setup"], json_data["punchline"]]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    text = data['text'].lower()

    if "play" in text and "video" in text:
        speak("You want me to play which video?")
        vid = text.replace("play video", "").strip()
        assist = Music()
        assist.play(vid)
        speak(f"Playing {vid} on YouTube")
        emit('response', {'message': f"Playing {vid} on YouTube"})

    elif "news" in text:
        speak("Sure, now I will read news for you.")
        arr = news()
        response = arr[:3]  # Only return the first 3 news items
        emit('response', {'message': response})

    elif "fact" in text or "facts" in text:
        x = randfacts.get_fact()  # Updated method
        speak("Did you know that, " + x)
        emit('response', {'message': "Did you know that, " + x})

    elif "joke" in text or "jokes" in text:
        speak("Sure, get ready for some laughs.")
        arr = joke()
        speak(arr[0])
        speak(arr[1])
        emit('response', {'message': arr[0] + " " + arr[1]})
 
    elif "information" in text:
        speak("You need information related to which topic?")
        infor = text.replace("information", "").strip()
        assist = Infow()
        assist.get_info(infor)
        speak(f"Searching {infor} on Wikipedia")
        emit('response', {'message': f"Searching {infor} on Wikipedia"})

    else:
        speak("I didn't understand that.")
        emit('response', {'message': "I didn't understand that."})

if __name__ == '__main__':
    socketio.run(app, debug=True)
