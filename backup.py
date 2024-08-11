import pyttsx3 as p
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import webbrowser
import subprocess
import randfacts
import requests
import time
import datetime
import sys
import random
import wikipedia
from wolframalpha import Client
from googlesearch import search

# Initialize the text-to-speech engine
engine = p.init()
engine.setProperty('rate', 170)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

# Wolfram Alpha API Key
wolfram_api_key = "your_wolfram_alpha_api_key"  # Replace with your actual Wolfram Alpha API Key

class Music:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def play(self, query):
        self.query = query
        self.driver.get("https://www.youtube.com/results?search_query=" + query)
        time.sleep(3)  # Give some time for the page to load
        videos = self.driver.find_element(By.XPATH, '//*[@id="dismissible"]/div')
        videos.click()

class Infow:
    def __init__(self):
        # Initialize Wolfram Alpha client
        self.wolfram_client = Client(wolfram_api_key)
    
    def get_info(self, query):
        # 1. Try Wolfram Alpha
        try:
            res = self.wolfram_client.query(query)
            answer = next(res.results).text
            return f"According to Wolfram Alpha: {answer}"
        except Exception:
            pass
        
        # 2. Try Wikipedia
        try:
            summary = wikipedia.summary(query, sentences=3)
            return f"According to Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Your query was ambiguous, here are some options: {e.options}"
        except wikipedia.exceptions.PageError:
            pass
        
        # 3. Fallback to Google Search
        try:
            search_results = list(search(query, num_results=1))
            if search_results:
                return f"I found this result: {search_results[0]}"
        except Exception as e:
            return f"An error occurred: {e}"

        return "Sorry, I couldn't find any information on that."

def joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    json_data = requests.get(url).json()
    arr = [json_data["setup"], json_data["punchline"]]
    return arr

def news():
    api_key = "da8f10bf8bb24d239a3ae495b767486d"
    api_address = f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={api_key}"
    json_data = requests.get(api_address).json()

    ar = []
    for i in range(3):
        ar.append("Number " + str(i+1) + ": " + json_data["articles"][i]["title"] + ".")
    return ar

def get_weather():
    api_key = "04c5779ab395db55356ebb3467424423"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_id = "1267701"  # Karnataka city ID for OpenWeatherMap
    complete_url = base_url + "appid=" + api_key + "&id=" + city_id

    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        try:
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            weather_info = (f"The temperature is {current_temperature - 273.15:.2f} degrees Celsius, "
                            f"pressure is {current_pressure} hPa, "
                            f"humidity is {current_humidity} percent, "
                            f"and the weather description is {weather_description}.")
            return weather_info
        except KeyError as e:
            return f"Error in fetching weather data: {e}"
    else:
        return "Sorry, I couldn't fetch the weather information."

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech(recognizer, source):
    try:
        audio = recognizer.listen(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Sorry, there was an issue with the request."

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning Simaan!")
    elif 12 <= hour < 18:
        speak("Good afternoon Simaan!")
    else:
        speak("Good evening Simaan!")

# Greet the user
greet_user()

# Announce the current time
current_time = datetime.datetime.now().strftime("%I:%M %p")
speak(f"The current time is {current_time}")

# Ask how to assist
speak("How can I assist you today?")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Start the command loop
while True:
    with sr.Microphone() as source:
        recognizer.energy_threshold = 10000
        recognizer.adjust_for_ambient_noise(source, 1.2)
        print("Listening...")
        command = recognize_speech(recognizer, source)
        print(f"User said: {command}")

        command_lower = command.lower()

        if "nothing" in command_lower or "exit" in command_lower:
            speak("Goodbye, Simaan!")
            sys.exit(0)
        elif "how are you" in command_lower:
            speak("I am also having a good day, love.")
        elif "information" in command_lower:
            speak("You need information related to which topic?")
            with sr.Microphone() as source:
                recognizer.energy_threshold = 10000
                recognizer.adjust_for_ambient_noise(source, 1.2)
                info_query = recognize_speech(recognizer, source)
                assist = Infow()
                info_text = assist.get_info(info_query)
                speak(f"Here is some information I found on {info_query}:")
                speak(info_text)
        elif "play" in command_lower and "video" in command_lower:
            speak("You want me to play which video?")
            with sr.Microphone() as source:
                recognizer.energy_threshold = 10000
                recognizer.adjust_for_ambient_noise(source, 1.2)
                video_query = recognize_speech(recognizer, source)
                assist = Music()
                assist.play(video_query)
                speak(f"Playing {video_query} on YouTube.")
        elif "news" in command_lower:
            speak("Sure, let me read the latest news for you.")
            latest_news = news()
            for item in latest_news:
                speak(item)
        elif "weather" in command_lower:
            speak("Sure, here is the weather information.")
            weather_forecast = get_weather()
            speak(f"The weather forecast is as follows: {weather_forecast}")
        elif "play music" in command_lower:
            speak("Opening Spotify for you.")
            # Open Spotify
            subprocess.Popen(["spotify"])  # Adjust if needed for your system
            time.sleep(5)  # Wait for Spotify to open

            # Optionally, you could send a command to play a specific track or playlist
            # Example Spotify URI: "spotify:track:TRACK_ID" or "spotify:playlist:PLAYLIST_ID"
            # Replace TRACK_ID or PLAYLIST_ID with actual IDs
            # spotify_uri = "spotify:track:TRACK_ID"
            # webbrowser.open(spotify_uri)

            speak("Spotify is now open. Please select your music.")
        elif "fact" in command_lower:
            speak("Sure, here's a fact for you.")
            fact = randfacts.getFact()
            speak(f"Did you know that, {fact}")
        elif "joke" in command_lower:
            speak("Sure, get ready for some laughs.")
            joke_text = joke()
            speak(joke_text[0])
            speak(joke_text[1])
        elif "open chrome" in command_lower:
            speak("Opening Chrome browser for you.")
            webbrowser.open("https://www.google.com")
        elif "open spotify" in command_lower:
            speak("Opening Spotify for you.")
            subprocess.Popen(["spotify"])  # Adjust the command if your system requires it
        elif "open youtube" in command_lower:
            speak("Opening YouTube for you.")
            webbrowser.open("https://www.youtube.com")
