#
#python -m venv env
#cd env  
#cd Script
#.\activate.bat
#python.exe -m pip install --upgrade pip
#pip install wolframalpha
#pip install pyttsx3
#pip install tkinter 
#pip install wikipedia
#pip install SpeechRecognition
#pip install ecapture
#pip install pyjokes
#pip install twilio
#pip install requests
#pip install pyjokes 
#pip install beautifulsoup4
#pip install winshell
#pip install feedparser
#pip install feedparser 
#pip install twilio 
#pip install clint
#pip install pipwin
#





import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen


engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Puedes ajustar la velocidad de habla si lo deseas
engine.setProperty('voice', 'spanish')  # Selecciona la voz en español
wikipedia.set_lang("es")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
 
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Buenos dias !")
  
    elif hour>= 12 and hour<18:
        speak("Buenas tardes !")   
  
    else: 
        speak("Buenas Noches !")  
  
    assname =("Alfredo")
    speak("Soy"+assname+"su asistente en el laboratorio")
    #speak(assname)
    
 
def username():
    speak("Cual es su nombre")
    uname = takeCommand()
    speak("Bienvenido al Centro de desarrollo tecnológico")
    speak(uname)
    columns = shutil.get_terminal_size().columns
     
    print("#####################".center(columns))
    print("Bienvenido.", uname.center(columns))
    print("#####################".center(columns))
     
    speak("Cómo puedo ayudarle")
 
def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=3)
    try:
        print("Reconociendo...")    
        query = r.recognize_google(audio, language ='es-ES')
        print(f"dijiste : {query}\n")
  
    except Exception as e:
        print(e)    
        print("Perdón, no entendí.")  
        return "None"
     
    return query
  
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
     
    # Enable low security in gmail
    server.login('adiaz', 'Intelig321!arti')
    server.sendmail('adiaz', to, content)
    server.close()

if __name__ == '__main__':
    clear = lambda: os.system('cls')    
    # Esta´función limpia el comando
    # antes de la ejecución de python
    clear()
    wishMe()
    username()
     
    while True:

        query = takeCommand().lower()
        print("paso", query)
        # All the commands said by user will be 
        # stored here in 'query' and will be
        # converted to lower case for easily 
        # recognition of command
        if 'wikipedia' in query:
            speak('Qué quieres buscar en Wikipedia...')
            query = takeCommand()
            results = wikipedia.summary(query, sentences = 1)
            speak("De acuerdo a Wikipedia")
            speak(results)
            speak('Puedes ir a la pagina de Wikipedia si deas más información')
            
        elif 'abra youtube' in query or 'abrir youtube' in query:
            speak("Aqui vas a Youtube\n")
            webbrowser.open("youtube.com")
        
        elif 'centro de desarrollo' in query or "cdt" in query or "cdt unab" in query or "soluciones iot" in query:
            speak("Te llevo a la página solicitada\n")
            webbrowser.open("https://apolo.unab.edu.co/es/organisations/centro-de-desarrollo-tecnol%C3%B3gico-smart-regions-center")
 
        elif ('smart region' in query or "smart region lab" in query) and 'página' in query:
            speak("Aqui vas a Smart Región Lab\n")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")

        elif ('smart region' in query or "smart region lab" in query) and ('objetivo' in query or 'misión' in query, 'página' in query or 'qué es' in query):
            speak("El Centro de Desarrollo Tecnológico (CDT) Smart Regions es un centro enfocado en el diseño y desarrollo de proyectos de CTeI, tecnologías propias y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico, articulando Sociedad, Estado, Empresa y Academia soportados en investigación y uso de tecnologías 4.0 para la transformación digital, creando valor sostenible y escalable para territorios inteligentes.\n")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")
            
        elif 'abra google' in query:
            speak("Vamos a  Google\n")
            webbrowser.open("google.com")
 

        elif 'escuchar musica' in query or "canción" in query or "musica" in query or "oir canción" in query:
            speak("Solo tengo esta canción porque mi jefe no me deja oir musica")
            # music_dir = "G:\\Song"
            music_dir = "D:\\asistente\musica"
            songs = os.listdir(music_dir)
            print(songs)    
            random = os.startfile(os.path.join(music_dir, songs[1]))
 
        elif 'fecha' in query or 'dime la hora' in query or 'dar la hora' in query:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")    
            speak(f"Sir, the time is {strTime}")
 
        #elif 'open opera' in query:
        #    codePath = r"C:\\Users\\GAURAV\\AppData\\Local\\Programs\\Opera\\launcher.exe"
        #    os.startfile(codePath)
 
        elif 'email al director' in query:
            try:
                speak("Qué quieres decile?")
                content = takeCommand()
                to = "adiaz@unab.edu.co"   
                sendEmail(to, content)
                speak("El email fué enviado !")
            except Exception as e:
                print(e)
                speak("No fué posible enviar el email, intenta más tarde")
 
        elif 'enviar email' in query or 'email' in query or 'enviar un email' in query:
            try:
                speak("Qué quiere decir?")
                content = takeCommand()
                speak("A quién desea enviale, escribe en la pantalla")
                to = input()    
                sendEmail(to, content)
                speak("El email fué enviado !")
            except Exception as e:
                print(e)
                speak("No fué posible enviar el email, intenta más tarde")
 
        elif 'cómo estás' in query:
            speak("Yo muy bien, gracias")
            speak("y usted qué tal?")
 
        elif 'bien' in query or "muy bien" in query:
            speak("Muy buen saber que estás bien")
 
        elif "cambiar tu nombre" in query or "cambie tu nombre" in query or "otro nombre para ti" in query:
            speak("Cual sería ni nuevo nombre")
            assname = takeCommand()
            speak("Gracias ahora soy"+assname)
 
 
        elif "cambiar nombre" in query or "cambie mi nombre" in query or "otro nombre" in query:
            speak("Cuál es tu nombre")
            uname = takeCommand()
            speak("Eres ahora"+uname)
 
        elif "cuál es tu nombre" in query or "qué  nombre" in query:
            speak("Mis amigos me llaman")
            speak(assname)
            print("My friends call me", assname)
 
        elif 'salir' in query:
            speak("Gracias por su tiempo")
            exit()
 
        elif "quien te construyo" in query or "quién te creó" in query: 
            speak("Yo fuí adaptado de un proyecto Gaurav, por Alfredo Diaz")
             
        elif 'chiste' in query:
            speak(pyjokes.get_joke(language='es', category= 'all'))
             
        elif "calculate" in query: 
             
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate') 
            query = query.split()[indx + 1:] 
            res = client.query(' '.join(query)) 
            answer = next(res.results).text
            print("The answer is " + answer) 
            speak("The answer is " + answer) 
 
        elif 'search' in query or 'play' in query:
             
            query = query.replace("search", "") 
            query = query.replace("play", "")          
            webbrowser.open(query) 
 
        elif "who i am" in query:
            speak("If you talk then definitely your human.")
 
        elif "why you came to world" in query:
            speak("Thanks to Gaurav. further It's a secret")
 
        elif 'power point presentation' in query:
            speak("opening Power Point presentation")
            power = r"C:\\Users\\GAURAV\\Desktop\\Minor Project\\Presentation\\Voice Assistant.pptx"
            os.startfile(power)
 
        elif 'is love' in query:
            speak("It is 7th sense that destroy all other senses")
 
        elif "who are you" in query:
            speak("I am your virtual assistant created by Gaurav")
 
        elif 'reason for you' in query:
            speak("I was created as a Minor project by Mister Gaurav ")
 
        elif 'change background' in query:
            ctypes.windll.user32.SystemParametersInfoW(20, 
                                                       0, 
                                                       "Location of wallpaper",
                                                       0)
            speak("Background changed successfully")
 
        elif 'open bluestack' in query:
            appli = r"C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe"
            os.startfile(appli)
 
        elif 'news' in query:
             
            try: 
                jsonObj = urlopen('''https://newsapi.org / v1 / articles?source = the-times-of-india&sortBy = top&apiKey =\\times of India Api key\\''')
                data = json.load(jsonObj)
                i = 1
                 
                speak('here are some top news from the times of india')
                print('''=============== TIMES OF INDIA ============'''+ '\n')
                 
                for item in data['articles']:
                     
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                 
                print(str(e))
 
         
        elif 'lock window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
 
        elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
                 
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")
 
        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)
 
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")
 
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")
 
        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
             
        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")
 
        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])
 
        elif "Escribe una nota" in query or "nota" in query:
            speak("Qué quisiera que yo escribiera")
            note = takeCommand()
            file = open('nota.txt', 'w')
            speak("Puedo incluir el dia y la hora")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
         
        elif "mostrar la nota" in query or "ver la nota" in query:
            speak("mostrando la nota")
            file = open("nota.txt", "r") 
            print(file.read())
            speak(file.read(6))
 
        elif "actualizar el asistente" in query:
            speak("After downloading file please replace this file with the downloaded one")
            url = '# url after uploading file'
            r = requests.get(url, stream = True)
             
            with open("Voice.py", "wb") as Pypdf:
                 
                total_length = int(r.headers.get('content-length'))
                 
                for ch in progress.bar(r.iter_content(chunk_size = 2391975),
                                       expected_size =(total_length / 1024) + 1):
                    if ch:
                      Pypdf.write(ch)
                     
        # NPPR9-FWDCX-D2C8J-H872K-2YT43
        elif "jarvis" in query:
             
            wishMe()
            speak("Jarvis 1 point o in your service Mister")
            speak(assname)
 
        elif "clima" in query:
             
            # Google Open weather website
            # to get API of Open weather 
            api_key = "b175155b402c44d69e3a12377008afca"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak(" Dime la ciudad ")
            print("El clima de : ")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url) 
            x = response.json() 
            print(response.text)
            if x["cod"] != "404": 
                y = x["main"] 
                current_temperature = str(float(y["temp"]) - 273.15 )
                current_pressure = y["pressure"] 
                current_humidity = y["humidity"] 
                z = x["weather"] 
                weather_description = z[0]["description"] 
                speak(" Temperatura (en Grados centígrados) = " +str(current_temperature)+"\n presión atmosférica (en hPa) ="+str(current_pressure) +"\n humedad (en percentage) = " +str(current_humidity) +"\n descripción = " +str(weather_description)) 
             
            else: 
                speak(" Ciudad no encontrada ")
             
        elif "enviar mensaje" in query:
                # You need to create an account on Twilio to use this service
                account_sid = 'Account Sid key'
                auth_token = 'Auth token'
                client = Client(account_sid, auth_token)
 
                message = client.messages \
                                .create(
                                    body = takeCommand(),
                                    from_='Sender No',
                                    to ='Receiver No'
                                )
 
                print(message.sid)
 
        elif "wikipedia" in query:
            webbrowser.open("wikipedia.com")
 
        elif "hola" in query or  "que tal" in query or "buenas" in query:
            speak("" +query)
            speak("Cómo estas?")
            speak(assname)
 
        # most asked question from google Assistant
        elif "seré tu novio" in query or "seré tu novia" in query:   
            speak("No puedo amar, así que mejor busque otra pareja, en qué te puedo ayudar")
 
        elif "cómo estás" in query:
            speak("Muy bien, gracias por preguntar")
 
        elif "te amo" in query:
            speak("Yo no puedo amar pero gracias por expresarlo, en qué te puedo ayudar")
 
        elif "qué es" in query or "quién es" in query or "hablame de" in query:
             
            # Use the same API key 
            # that we have generated earlier
            client = wolframalpha.Client("3527QJ-EYKJ9QYEQY")
            res = client.query(query)
             
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No tengo resutados para esa pregunta")
                speak ("No encontré una respuesta, intenta otra vez")
 
        # elif "" in query:
            # Command go here
            # For adding more commands
    
    
