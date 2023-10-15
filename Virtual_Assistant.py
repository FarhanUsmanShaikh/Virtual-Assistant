# Import necessary libraries
import pyttsx3  # For text-to-speech functionality
import speech_recognition as sr  # For speech recognition
import datetime  # For working with date and time
import wikipedia  # For searching on Wikipedia
import webbrowser  # For opening websites in a browser
import os  # For opening applications and files
import requests  # For making API requests to get weather information
import math  # For mathematical calculations
import pygame  # For playing music
import smtplib  # For sending emails
import getpass  # For securely entering email password

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to speak (convert text to speech)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to greet the user based on the time of day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Your Virtual Assistant. Please tell me how may I help you")

# Function to recognize and capture user's voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

# Function to get weather information for a specified city
def get_weather(city):
    api_key = '6a3b7fc29dfee8627f686a38cd9ae2e9'
    units = 'metric'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
    try:
        response = requests.get(url)
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        speak(f"The weather in {city} is currently {weather_description}.")
        speak(f"The temperature is {temperature} degrees Celsius.")
        speak(f"The humidity is {humidity}%.")

    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I couldn't fetch the weather information for that location.")

# Function to send an email
def send_email(subject, message, to_email):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        sender_email = input("Enter your email: ")
        password = getpass.getpass("Enter your email password: ")
        server.login(sender_email, password)
        email_text = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, email_text)
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I couldn't send the email.")

# Main program execution
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Wikipedia search functionality
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Open various websites in the browser
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'open plus' in query:
            webbrowser.open("C:/Program Files/Notepad++/notepad++.exe")

        elif 'open notepad' in query:
            webbrowser.open("C:/Windows/System32/notepad.exe")

        elif 'code' in query:
            webbrowser.open("C:/Users/DELL/AppData/Local/Programs/Microsoft VS Code/Code.exe")

        # Get and speak the current time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        # Open Visual Studio Code
        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        # Weather functionality
        elif 'weather' in query:
            speak("Sure, which city's weather would you like to know?")
            city = takeCommand().lower()
            get_weather(city)

        # Mathematical calculations
        elif 'calculate' in query:
            expression = query.replace("calculate", "").strip()
            try:
                result = eval(expression)
                speak(f"The result of {expression} is {result}")
            except Exception as e:
                speak("Sorry, I couldn't calculate the result.")

        # Play Music using pygame
        elif 'play music' in query:
            music_file = 'path_to_your_music_file.mp3'  # Replace with the path to your music file
            pygame.mixer.init()
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()

        # Email functionality
        elif 'send email' in query:
            try:
                speak("What should the email say?")
                email_message = takeCommand()

                speak("What is the subject of the email?")
                email_subject = takeCommand()

                speak("To whom should I send the email?")
                recipient_email = input("Enter the recipient's email address: ")

                send_email(email_subject, email_message, recipient_email)
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("Sorry, I couldn't send the email.")

        else:
            print("No query matched")