#
#python -m venv env
#cd env  
#cd Script
#.\activate.bat
#python.exe -m pip install --upgrade pip
#pip install wolframalpha
#pip install pyttsx3
#pip install tkinter  No instalado
#pip install wikipedia
#pip install SpeechRecognition
#pip install ecapture
#pip install pyjokes
#pip install twilio
#pip install requests
#pip install beautifulsoup4
#pip install winshell
#pip install feedparser
#pip install clint
#pip install pyaudio
#pip install pipwin




import subprocess
import wolframalpha
import pyttsx3
#import tkinter
import json
#import random
#import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
#import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
#from bs4 import BeautifulSoup
#import win32com.client as wincl
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
    print("          Bienvenido.".center(columns), uname.center(columns))
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
    server = smtplib.SMTP('smtp.gmail.com', 465)
    server.ehlo()
    server.starttls()
     
    # Enable low security in gmail
    server.login('adiaz@unab.edu.co', 'Intelig321!Arti')
    server.sendmail('adiaz@unab.edu.co', to, content)
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
            speak('Puedes ir a la página de Wikipedia si das más información')
            
        elif 'abra youtube' in query or 'abrir youtube' in query or 'youtube' in query:
            speak("Aqui vas a Youtube\n")
            webbrowser.open("youtube.com")
        
        elif 'centro de desarrollo' in query or "cdt" in query or "cdt unab" in query or "soluciones iot" in query or "desarrollo tecnológico" in query:
            speak('Los centros de de desarrollo tecnológico son organizaciones públicas o privadas, dedicadas al desarrollo de proyectos de investigación aplicada, el desarrollo de tecnología propia y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico del país, sus regiones y/o ciudades.')
            speak("Te llevo auna página que te sirve de referencia\n")
            webbrowser.open("https://apolo.unab.edu.co/es/organisations/centro-de-desarrollo-tecnol%C3%B3gico-smart-regions-center")
 
        elif ('smart region' in query or "smart region lab" in query or "smart región lab" in query or  "smar región lab" in query) and 'página' in query:
            speak("Aqui vas a la página de Smart Región Lab\n")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")

        elif ('smart región' in query or "smart región lab" in query) and ('objetivo' in query or 'misión' in query or 'página' in query or 'qué es' in query or 'que es' in query):
            speak("El Centro de Desarrollo Tecnológico (CDT) Smart Regions es un centro enfocado en el diseño y desarrollo de proyectos de CTeI, tecnologías propias y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico, articulando Sociedad, Estado, Empresa y Academia soportados en investigación y uso de tecnologías 4.0 para la transformación digital, creando valor sostenible y escalable para territorios inteligentes.\n")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")

        elif ('áreas'  in query or 'temas' in query) and ('cdt' in query or 'laboratorio' in query or 'Smart' in query or 'región' in query or 'que es' in query):
            speak("El Centro de Desarrollo Tecnológico (CDT) Smart Regions es un centro enfocado en el diseño y desarrollo de proyectos de CTeI, tecnologías propias y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico, articulando Sociedad, Estado, Empresa y Academia soportados en investigación y uso de tecnologías 4.0 para la transformación digital, creando valor sostenible y escalable para territorios inteligentes.\n")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")


        elif ('focos' in query or "foco" in query) and ('cdt' in query or 'laboratorio' in query or 'smart' in query or 'region' in query or 'que es' in query):
            speak("El Centro de Desarrollo Tecnológico (CDT) Smart Regions es un centro enfocado en el diseño y desarrollo de proyectos de CTeI, tecnologías propias y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico, articulando Sociedad, Estado, Empresa y Academia soportados en investigación y uso de tecnologías 4.0 para la transformación digital, creando valor sostenible y escalable para territorios inteligentes.\n")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")

        elif ('tecnologias' in query or "tecologia" in query) and ('cdt' in query or 'laboratorio' in query or 'smart' in query or 'region' in query or 'que es' in query):
            speak("El Centro de Desarrollo Tecnológico (CDT) Smart Regions es un centro enfocado en el diseño y desarrollo de proyectos de CTeI, tecnologías propias y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico, articulando Sociedad, Estado, Empresa y Academia soportados en investigación y uso de tecnologías 4.0 para la transformación digital, creando valor sostenible y escalable para territorios inteligentes.\n")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")


        elif 'abra google' in query or 'ir a google' in query or 'google' in query:
            speak("Quiere ir a Google, aquí tienes \n")
            webbrowser.open("google.com")
 

        elif 'escuchar música' in query or "canción" in query or "música" in query or "oir una canción" in query:
            speak("Solo tengo esta canción porque mi jefe no me deja oir musica")
            # music_dir = "G:\\Song"
            music_dir = "D:\\asistente\\musica"
            songs = os.listdir(music_dir)
            print(songs)    
            random = os.startfile(os.path.join(music_dir, songs[1]))
 
        elif 'fecha' in query or 'dame la hora' in query or 'dame la fecha' in query or 'hora' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")   
            speak(f"La fecha y hora son {strTime}")
 
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
 
        elif 'cómo estás' in query or 'qué tal estás'in query  or  'qué tal'in query:
            speak("Yo muy bien, gracias")
            speak("Espero que usten tabiém?")
 
        elif 'yo bien' in query or "muy bien" in query or "estoy bien" in query:
            speak("Muy buen saber que estás bien")
 
        elif "cambiar tu nombre" in query or "cambie tu nombre" in query or "otro nombre para ti" in query:
            speak("Cual sería mi nuevo nombre")
            assname = takeCommand()
            speak("Gracias ahora soy"+assname)
 
 
        elif "cambiar nombre" in query or "cambie mi nombre" in query or "otro nombre" in query:
            speak("Cuál es tu nombre")
            uname = takeCommand()
            speak("Eres ahora"+uname)
 
        elif "cuál es tu nombre" in query or "qué nombre tienes" in query:
            speak("Mis amigos me llaman")
            speak(assname)
            print("Mis amigos me llaman", assname)
 
        elif 'salir' in query:
            speak("Gracias por su tiempo")
            exit()
 
        elif "quien te construyó" in query or "quién te creó" in query: 
            speak("Yo fuí adaptado y entrenado por Alfredo Diaz del Centro de desarrollo tecnológico")
             
        elif 'chiste' in query:
            speak(pyjokes.get_joke(language='es', category= 'all'))
             
        elif "calcula" in query or "operación matemática" in query  : 
             
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client("3527QJ-EYKJ9QYEQY")
            indx = query.lower().split().index('calculate') 
            query = query.split()[indx + 1:] 
            res = client.query(' '.join(query)) 
            answer = next(res.results).text
            print("La respuesta es" + answer) 
            speak("La respuesta es" + answer) 
 
        elif 'buscar' in query or 'encuentre' in query:
             
            query = query.replace("search", "") 
            query = query.replace("play", "")          
            webbrowser.open(query) 
 
        elif "quién soy yo" in query:
            speak("Si estas hablando eres un humano.")
 
        elif "Por qué vino" in query or "A qué vino" in query  or "A qué vino a este mundo" in query  or "por que nació" in query  or "porque nació" in query:
            speak("Vine a este mundo gracias al trabajo de Alfredo, estoy entrenado para ti")
 
        elif 'presentación' in query or 'presentacion' in query:
            speak("Abriendo la presentación de Power Point")
            power = r"C:\\Users\\Usuario\\Documents\\Proyecto IA\\asistente\\presentacion\\Voice Assistant.pptx"
            os.startfile(power)
 
        elif 'qué es amor' in query or 'que es amor' in query or 'Qué es amor' in query:
            speak("Es el séptimo sentido que destruye a los otros sentidos. es un chiste")
 
        elif "quién eres" in query or 'quién eres' in query or 'Quién eres' in query:
            speak("Yo soy el asistente virtual del Smart Region Lab entrenado por Alfredo")
 
        elif 'Para qué te crearon' in query or 'Por qué te crearon' in query:
            speak("Fuí creado para un experimento en el laboratorio Smart Region Lab por Alfredo")
 
        #elif 'change background' in query:
        #    ctypes.windll.user32.SystemParametersInfoW(20, 
        #                                               0, 
        #                                               "Location of wallpaper",
        #                                               0)
        #    speak("Background changed successfully")
        # 
        #elif 'open bluestack' in query:
        #    appli = r"C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe"
        #    os.startfile(appli)
 
        elif 'noticia' in query:
             
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
 
         
        elif 'bloquea la pantalla' in query or 'bloquea windows' in query:
                speak("Bloquendo windows")
                ctypes.windll.user32.LockWorkStation()
 
        elif 'bajar el sistema' in query:
                speak("Espera un segundo ! Su sistema está en camino de apagarse")
                subprocess.call('shutdown / p /f')
                 
        elif 'borra reciclaje' in query or 'limpia el reciclaje' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Reciclaje borrado")
 
        elif "no escuchar" in query or "pare de escuchar" in query:
            speak("¿Durante cuánto tiempo deseas que  deje de escuchar comandos?")
            a = int(takeCommand())
            time.sleep(a)
            print(a)
 
        elif "dónde estamos" in query:
            query = query.replace("donde estamos", "")
            location = query
            speak("Vamos a ubicar")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location + "")
 
        elif "cámara" in query or "tomar una foto" in query:
            ec.capture(0, "foto", "img.jpg")
 
        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
             
        elif "hibernar" in query or "sleep" in query:
            speak("Hibernando")
            subprocess.call("shutdown / h")
 
        elif "cerrar sesión" in query or "sign out" in query:
            speak("Asegúrese de que todas las aplicaciones estén cerradas antes de cerrar sesión.")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])
 
        elif "escribe una nota" in query or "escribir nota" in query:
            speak("Qué quisiera que yo escribiera")
            note = takeCommand()
            file = open('nota.txt', 'w')
            speak("Puedo incluir el dia y la hora")
            snfm = takeCommand()
            if 'si' in snfm or 'seguro' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
         
        elif "mostrar la nota" in query or "ver la nota" in query or "ver nota" in query:
            speak("mostrando la nota")
            file = open("nota.txt", "r") 
            print(file.read())
            speak(file.read(6))
 
        elif "actualizar el asistente" in query:
            speak("Después de descargar el archivo, reemplace este archivo con el descargado.")
            url = 'https://raw.githubusercontent.com/adiacla/asistente/main/'
            r = requests.get(url, stream = True)
             
            with open("asistente.py", "wb") as Pypdf:
                 
                total_length = int(r.headers.get('content-length'))
                 
                for ch in progress.bar(r.iter_content(chunk_size = 2391975),
                                       expected_size =(total_length / 1024) + 1):
                    if ch:
                      Pypdf.write(ch)
                     
        # NPPR9-FWDCX-D2C8J-H872K-2YT43
        elif "alfredo" in query:
             
            wishMe()
            speak("Si señor ese soy yo... ")
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
                current_temperature = str(round(float(y["temp"] - 273.15 ),0))
                current_pressure = y["pressure"] 
                current_humidity = y["humidity"] 
                z = x["weather"] 
                weather_description = z[0]["description"] 
                speak(" Temperatura es= " +str(current_temperature)+"grados centigrados"+"\n presión atmosférica="+str(current_pressure) +"hpa"+"\n la humedad es= " +str(current_humidity)+"porciento") 
             
            else: 
                speak(" la ciudad no fué encontrada ")
             
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
            client = wolframalpha.Client("3527QJ-EYKJ9QYEQY",location="bucaramanga,CO")
            res = client.query(query)
             
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No tengo resultados para esa pregunta")
                speak ("No encontré una respuesta, intenta otra vez")
 
        # elif "" in query:
            # Command go here
            # For adding more commands
    
    
    
