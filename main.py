import pyttsx3
import time
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from googlesearch import search
import requests
import json
import config

# Initializing TTS engine
engine = pyttsx3.init()

# Checking for the available voices
voices = engine.getProperty("voices")

# printing available voices
# i = 1
# for voice in voices:
#     print(f"Voice{i} : ")
#     print("ID: ", voice.id)
#     print("Name: ", voice.name)
#     print("\n")
#     i = i + 1


# print(type(voices))
# So the type of voices variable is "List"

# Setting Properties
engine.setProperty("voice", voices[1].id)
#150 Words per minute.
engine.setProperty('rate', 150) 


def greet():
    hour = int(time.strftime('%H'))
    if(hour < 12):
        engine.say("Good Morning. I am your virtual assistant. How may I help you?")
    elif((hour >= 12) & (hour < 17)):
        engine.say("Good Afternoon. I am your virtual assistant. How may I help you?")
    elif((hour >= 17) & (hour < 19)):
        engine.say("Good Evening. I am your virtual assistant. How may I help you?")
    else:
        engine.say("Good Night. I am your virtual assistant. How may I help you?")



def take_command():
    '''It takes microphone input from the user and returning it in string format.'''
    # sr is a speech Recognization module, where Recognizer is a class in it.
    print("\n")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.energy_threshold = 400  # minimum audio energy to consider for recording
        r.pause_threshold = 0.6  # Set the pause threshold to 0.6 seconds
        r.dynamic_energy_adjustment_ratio = 1.5  # Adjust the dynamic energy adjustment ratio
        r.dynamic_energy_adjustment_damping = 0.15  # Adjust the dynamic energy adjustment damping
        audio = r.listen(source, timeout=2.0)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio_data = audio, language = "en-in")
        print("User said: ", query)
    except Exception as e:
        # print(e)
        print("Sorry!! Can you please say it again.")
        return "None"
    return query


def get_weather(city):
    api_key = config.weather_api_keys
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    complete_url = f"{base_url}?q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    # print(data)  # Print the JSON response for debugging
    
    if data["cod"] == "404":
        return "City not found"
    
    weather_info = data["main"]
    temperature = weather_info["temp"]
    humidity = weather_info["humidity"]
    description = data["weather"][0]["description"]
    return f"The current weather in {city} is {description}. Temperature: {temperature}°C, Humidity: {humidity}%."


if __name__ == "__main__":
    greet()
    engine.runAndWait()
    while True:
        query = take_command().lower()

        if "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "open gmail" in query:
            webbrowser.open("gmail.com")

        elif "time" in query:
            t = time.strftime('%H:%M')
            print(t)
            engine.say(t)
            engine.runAndWait()

        elif "date" in query:
            d = time.strftime('%d-%m-%y')
            print(d)
            engine.say(d)
            engine.runAndWait()

        elif "code" in query:
            path = "C:\\Users\\asus\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(path)

        elif "quit" in query:
            break

        elif "weather" in query:
            print("Getting weather information...")
            city = query.replace("weather", "")
            weather_result = get_weather(city)
            print(weather_result)
            engine.say(weather_result)
            engine.runAndWait()

        else:
            try:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences = 3)
                print(results)
                engine.say(results)
                engine.runAndWait()
            except Exception as e:
                engine.say("Sorry, Right now i cant process your query.")

     
