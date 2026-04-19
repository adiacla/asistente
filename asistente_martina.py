"""
╔══════════════════════════════════════════════════════════════════╗
║          MARTINA - Asistente Virtual con Voz y Avatar           ║
║          Smart Regions Center - CDT UNAB                        ║
║                                                                  ║
║  Autor: Alfredo Díaz Claro                                       ║
║  Centro de Desarrollo Tecnológico Smart Regions Center           ║
║  Universidad Autónoma de Bucaramanga - UNAB                      ║
║  Contacto: adiaz@unab.edu.co                                     ║
║  Versión: 2.0 | 2026                                             ║
╚══════════════════════════════════════════════════════════════════╝

Descripción:
    Asistente de voz tipo Alexa especializado en información del CDT
    Smart Regions Center. Incluye avatar animado sincronizado con la
    voz, reconocimiento de voz natural, y respuestas inteligentes
    basadas en la base de conocimiento del centro.

Activación: Di "Martina" para activar el asistente.
"""

import tkinter as tk
from tkinter import font as tkfont
import threading
import time
import datetime
import os
import json
import re
import webbrowser
import smtplib
import requests
import wikipedia
import pyttsx3
import speech_recognition as sr
import pyjokes
from PIL import Image, ImageTk

# ── Módulo de música en streaming ────────────────────────────────
try:
    from musica import PlayerMusica, interpretar_comando_musica
    MUSICA_DISPONIBLE = True
except ImportError:
    MUSICA_DISPONIBLE = False

# ── Configuración global ──────────────────────────────────────────

WAKE_WORD       = "martina"           # Palabra de activación
ASSISTANT_NAME  = "Martina"
BOT_COLOR       = "#1B3A5C"           # Azul oscuro institucional
ACCENT_COLOR    = "#00A896"           # Verde tecnológico
TEXT_COLOR      = "#F5F5F5"
BG_COLOR        = "#0D1B2A"
CARD_COLOR      = "#1E2D3D"

IMAGES_DIR      = "images"            # Carpeta con los avatares
IMG_OPEN        = os.path.join(IMAGES_DIR, "bocaabiertaf.png")
IMG_CLOSED      = os.path.join(IMAGES_DIR, "bocacerradaf.png")
IMG_LISTEN      = os.path.join(IMAGES_DIR, "bocacerradaf.png")  # Puedes agregar imagen de escucha

import os
from dotenv import load_dotenv

load_dotenv()  # Carga el archivo .env automáticamente

HF_API_TOKEN    = os.getenv("HF_API_TOKEN", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
EMAIL_PASSWORD  = os.getenv("EMAIL_PASSWORD", "")

# ── Motor TTS ─────────────────────────────────────────────────────

engine = pyttsx3.init()
engine.setProperty('rate', 145)
engine.setProperty('volume', 1.0)

# Seleccionar voz en español (mujer si existe)
voices = engine.getProperty('voices')
voz_seleccionada = None
for v in voices:
    nombre = v.name.lower()
    lang   = "".join(str(v.languages)).lower()
    if 'spanish' in lang or 'es_' in lang or 'sabina' in nombre or 'helena' in nombre:
        voz_seleccionada = v.id
        break
if voz_seleccionada:
    engine.setProperty('voice', voz_seleccionada)

wikipedia.set_lang("es")

# ── Base de conocimiento del CDT ──────────────────────────────────
# Cubre las 50 preguntas y respuestas del documento oficial del CDT
# Smart Regions Center — UNAB

CONOCIMIENTO_CDT = {

    # ── Categoría 1: Información General y Misión ─────────────────
    "qué es el cdt":
        "Somos el Centro de Desarrollo Tecnológico Smart Regions Center, "
        "enfocado en crear soluciones de Internet de las Cosas para los "
        "sectores estratégicos del departamento de Santander.",

    "qué es smart regions":
        "El Smart Regions Center es un Centro de Desarrollo Tecnológico "
        "que crea soluciones IoT para los sectores estratégicos de Santander, "
        "bajo el concepto de territorios inteligentes o Smart Cities.",

    "universidad pertenece":
        "Nuestra entidad ejecutora es la Universidad Autónoma de "
        "Bucaramanga, conocida como UNAB.",

    "misión":
        "Nuestra misión es contribuir al desarrollo y modernización "
        "tecnológica de la región, posicionándola como referente en innovación.",

    "visión":
        "Buscamos consolidar a Santander como una región donde la tecnología "
        "sea prioridad para la competitividad.",

    "territorios inteligentes":
        "Trabajamos bajo el concepto de Smart Cities, integrando tecnologías "
        "digitales para mejorar la calidad de vida y la eficiencia en el entorno.",

    "cómo se articula":
        "Nos articulamos mediante un esfuerzo colaborativo entre diversas "
        "instituciones para unir capacidades e intereses regionales, "
        "articulando Sociedad, Estado, Empresa y Academia.",

    "cuándo inició":
        "El proyecto fue radicado el 26 de noviembre de 2019 e inició "
        "su ejecución formal el 21 de febrero de 2022.",

    "quién conforma":
        "Somos un equipo apasionado de profesionales dedicados a hacer "
        "la diferencia a través de la tecnología.",

    # ── Categoría 2: Servicios y Tecnologías 4.0 ─────────────────
    "servicios":
        "Prestamos servicios de ejecución técnica y científica en procesos "
        "involucrados en el desarrollo de soluciones tecnológicas: "
        "vigilancia tecnológica, prototipado, maduración de tecnologías, "
        "implementación de soluciones IoT, e integración de Inteligencia Artificial.",

    "tecnologías":
        "Nos especializamos en Internet de las Cosas y la integración de "
        "Inteligencia Artificial. También trabajamos en Ciencia de Datos, "
        "Simulación, Ciberseguridad, Robótica y Ciudades Inteligentes.",

    "vigilancia tecnológica":
        "Es una herramienta que utilizamos para delimitar necesidades "
        "y especificaciones técnicas en el ecosistema de innovación.",

    "prototipado":
        "Sí, contamos con capacidades para la programación y ejecución "
        "de prototipos y soluciones tecnológicas.",

    "maduración tecnologías":
        "Realizamos diagnósticos de madurez tecnológica y diseñamos rutas "
        "de fortalecimiento especializado y pilotaje.",

    "soluciones iot":
        "Desarrollamos soluciones IoT personalizadas para los sectores "
        "productivos de la región de Santander.",

    "inteligencia artificial":
        "Integramos IA en el diseño y generación de soluciones para "
        "proyectos de Ciencia, Tecnología e Innovación.",

    "implantación tecnología":
        "Es el proceso de poner en marcha e implementar la solución "
        "que atiende la necesidad identificada en una organización.",

    # ── Categoría 3: Sectores Estratégicos y Proyectos ───────────
    "sectores":
        "Nos enfocamos en seis sectores estratégicos: Agroindustria, "
        "Biodiversidad y Biotecnología, Energía, Salud, Manufactura y Turismo.",

    "sector salud":
        "Colaboramos con entidades como la Fundación Cardiovascular de Colombia "
        "y participamos en encuentros internacionales de investigación en salud.",

    "turismo":
        "Desarrollamos el proyecto Conexión Natural, que integra tecnologías "
        "digitales para potenciar el turismo de naturaleza en municipios "
        "como Río de Oro, en el Cesar.",

    "biodiversidad":
        "Trabajamos en el monitoreo de biofertilizantes e investigaciones "
        "científicas aplicadas a la biodiversidad.",

    "energía":
        "Contamos con una plataforma de compra y venta de energía tipo "
        "P2P, diseñada para facilitar transacciones entre pares dentro "
        "de comunidades energéticas.",

    "monitoreo agrícola":
        "Aplicamos tecnologías de la Industria 4.0 para mejorar los "
        "procesos en agronegocios.",

    "conexión natural":
        "Es una iniciativa que utiliza tecnologías digitales para fortalecer "
        "el turismo de naturaleza en el municipio de Río de Oro, en el Cesar.",

    "río de oro":
        "Río de Oro es el municipio del Cesar donde desarrollamos el proyecto "
        "Conexión Natural de turismo de naturaleza con tecnología digital.",

    # ── Categoría 4: Aliados y Colaboraciones ────────────────────
    "aliados":
        "Nuestros aliados principales son la Cámara de Comercio de Bucaramanga, "
        "UNIRED, Phina Biosoluciones S.A.S. y la Cámara de Comercio "
        "de Barrancabermeja.",

    "unired":
        "UNIRED es un aliado estratégico clave que ha colaborado por años "
        "para alcanzar hitos tecnológicos en Santander.",

    "phina biosoluciones":
        "Phina Biosoluciones es una de las empresas aliadas que participa "
        "activamente en la conformación y desarrollo de nuestras soluciones IoT.",

    "beneficios colaboraciones":
        "Las colaboraciones estratégicas permiten ampliar horizontes, "
        "compartir recursos y crear soluciones innovadoras de mayor valor.",

    "minciencias":
        "Nuestro centro fue creado bajo convocatorias de lo que hoy es "
        "MinCiencias y financiado con recursos del Sistema General de Regalías.",

    "financiación":
        "El centro fue financiado con recursos del Sistema General de "
        "Regalías, bajo convocatorias de MinCiencias.",

    # ── Categoría 5: Formación y Talento Humano ──────────────────
    "entrenamiento formación":
        "Brindamos acompañamiento en la ejecución científica y técnica "
        "a través de nuestros equipos de investigación.",

    "talento humano":
        "Uno de nuestros objetivos principales es instalar capacidades "
        "de innovación en el talento humano de la región.",

    "semilleros investigación":
        "Participamos en encuentros internacionales para reunir a semilleros "
        "en torno a la innovación tecnológica.",

    # ── Categoría 6: Contacto, Ubicación y Participación ─────────
    "ubicación":
        "Nuestra oficina se encuentra en la Avenida 42 número 48 guion 11, "
        "en Bucaramanga, Colombia.",

    "contacto":
        "Puedes llamarnos al 6 4 3 6 1 1 1 extensión 4 2 3, "
        "o escribir a smartregions arroba unab punto edu punto co.",

    "teléfono":
        "Puedes llamarnos al 6 4 3 6 1 1 1 extensión 4 2 3.",

    "correo electrónico":
        "Escríbenos a smartregions arroba unab punto edu punto co.",

    "convocatorias":
        "Puedes encontrar las convocatorias vigentes en la sección de "
        "convocatorias de nuestro sitio web oficial.",

    "trabajo empleo":
        "Publicamos vacantes para investigadores y coinvestigadores en "
        "nuestra sala de prensa y redes sociales.",

    "smart center lab":
        "Es nuestro laboratorio dedicado a la innovación, resultado de "
        "años de esfuerzo colaborativo institucional. Cuenta con áreas "
        "de ideación, diseño, prototipado, desarrollo electrónico, "
        "manufactura y prueba de concepto.",

    "laboratorio":
        "El Smart Center Lab es nuestro laboratorio de innovación. "
        "Cuenta con áreas de ideación, diseño, prototipado, desarrollo "
        "electrónico, manufactura y prueba de concepto.",

    "casos de éxito":
        "Contamos con experiencias documentadas de aliados como "
        "Penagos Hermanos y la Universidad Santo Tomás.",

    "penagos hermanos":
        "Penagos Hermanos es uno de nuestros casos de éxito documentados "
        "en el desarrollo de soluciones tecnológicas.",

    "suscribirse noticias":
        "Puede registrar su correo electrónico en nuestro sitio web "
        "para recibir las últimas noticias del CDT.",

    "sitio web":
        "Visítenos en smartregionscenter punto com punto co",

    "página web":
        "Nuestra página web es smartregionscenter punto com punto co, "
        "donde encontrará toda la información del centro.",

    "redes sociales":
        "Nos encuentras en nuestras redes sociales donde publicamos "
        "las últimas noticias, vacantes y proyectos del CDT.",

    "quién te creó":
        "Fui creada por Alfredo Díaz Claro, del Centro de Desarrollo "
        "Tecnológico Smart Regions Center de la UNAB. "
        "Aún soy joven y aprendo cada día.",

    "objetivo laboratorio":
        "El CDT Smart Regions es un centro enfocado en el diseño y "
        "desarrollo de proyectos de CTeI, tecnologías propias y actividades "
        "de transferencia, articulando Sociedad, Estado, Empresa y Academia "
        "con tecnologías 4.0 para la transformación digital.",

    "temas laboratorio":
        "Los temas que cubre el CDT son: Estructuración de proyectos de "
        "I+D+I, Entrenamiento y formación especializada, Diseño y desarrollo "
        "de soluciones tecnológicas, Vigilancia Tecnológica e Inteligencia "
        "Competitiva, y Consultoría especializada en innovación.",
}


def buscar_en_conocimiento(query: str) -> str | None:
    """
    Busca en la base de conocimiento del CDT.

    Sistema de puntuación de 3 niveles:
    1. Coincidencia exacta de la clave completa en la query  → score alto
    2. Cada palabra de la clave que aparece en la query       → score medio
    3. Cada palabra de la query que aparece en la respuesta   → score bajo (desempate)

    Esto evita que siempre gane la primera entrada del diccionario.
    """
    query_lower = query.lower()

    stopwords = {
        'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'en', 'es',
        'qué', 'que', 'cuál', 'cual', 'cómo', 'como', 'tiene', 'hay',
        'por', 'para', 'con', 'su', 'me', 'te', 'se', 'al', 'yo', 'tú',
        'sobre', 'dime', 'cuéntame', 'quiero', 'saber', 'más', 'puedes',
        'hay', 'del', 'nos', 'también', 'esto', 'ese', 'esa'
    }

    palabras_query = set(re.findall(r'\w+', query_lower)) - stopwords

    mejor_match = None
    mejor_score = 0

    for clave, respuesta in CONOCIMIENTO_CDT.items():
        score = 0
        palabras_clave = set(re.findall(r'\w+', clave.lower())) - stopwords

        # Nivel 1: clave completa aparece como frase en la query (máxima prioridad)
        if clave.lower() in query_lower:
            score += 100

        # Nivel 2: cada palabra de la clave que aparece en la query
        coincidencias_clave = palabras_query & palabras_clave
        score += len(coincidencias_clave) * 10

        # Nivel 2b: cada palabra de la query que aparece en la clave
        # (captura casos como "misión del CDT" → clave "misión")
        for palabra in palabras_query:
            if palabra in clave.lower():
                score += 8

        # Nivel 3: palabras de la query en la respuesta (desempate)
        palabras_respuesta = set(re.findall(r'\w+', respuesta.lower())) - stopwords
        score += len(palabras_query & palabras_respuesta) * 1

        if score > mejor_score:
            mejor_score = score
            mejor_match = respuesta

    # Umbral mínimo de 8 puntos (al menos 1 palabra de la clave coincide)
    if mejor_score >= 8:
        return mejor_match
    return None


# ── Interfaz gráfica (Tkinter) ────────────────────────────────────

class MartinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Martina — Smart Regions Center")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Estado
        self.hablando    = False
        self.escuchando  = False
        self.activa      = False
        self.mostrar_texto_var = tk.BooleanVar(value=True)

        # Player de música
        self.player_musica = None
        if MUSICA_DISPONIBLE:
            self.player_musica = PlayerMusica(callback_hablar=None)

        # Cargar imágenes del avatar
        self._cargar_imagenes()

        # Construir UI
        self._build_ui()

        # Calibrar micrófono una sola vez (ahorra ~0.4s por escucha)
        self._energy_threshold = 300
        threading.Thread(target=self._calibrar_microfono, daemon=True).start()

        # Iniciar motor de escucha en hilo separado
        self._tts_lock = threading.Lock()
        threading.Thread(target=self._motor_principal, daemon=True).start()

    # ── Carga de imágenes ─────────────────────────────────────────

    def _cargar_imagenes(self):
        try:
            img_open   = Image.open(IMG_OPEN).resize((280, 280), Image.LANCZOS)
            img_closed = Image.open(IMG_CLOSED).resize((280, 280), Image.LANCZOS)
            self.img_open   = ImageTk.PhotoImage(img_open)
            self.img_closed = ImageTk.PhotoImage(img_closed)
        except Exception:
            # Fallback: círculos de color si no hay imágenes
            self.img_open   = None
            self.img_closed = None

    # ── Construcción de la UI ─────────────────────────────────────

    def _build_ui(self):
        W = 480

        # ── Encabezado ──────────────────────────────────────────
        header = tk.Frame(self.root, bg=BOT_COLOR, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header, text="MARTINA",
            font=("Helvetica Neue", 22, "bold"),
            bg=BOT_COLOR, fg=ACCENT_COLOR
        ).pack()
        tk.Label(
            header,
            text="Asistente Virtual · Smart Regions Center · UNAB",
            font=("Helvetica Neue", 9),
            bg=BOT_COLOR, fg="#A0B4C8"
        ).pack()

        # ── Avatar ──────────────────────────────────────────────
        avatar_frame = tk.Frame(self.root, bg=BG_COLOR, pady=18)
        avatar_frame.pack()

        if self.img_closed:
            self.avatar_lbl = tk.Label(
                avatar_frame, image=self.img_closed, bg=BG_COLOR
            )
        else:
            # Círculo de color como placeholder
            canvas = tk.Canvas(avatar_frame, width=280, height=280,
                               bg=BG_COLOR, highlightthickness=0)
            canvas.create_oval(10, 10, 270, 270, fill=ACCENT_COLOR, outline="")
            canvas.create_text(140, 140, text="M", fill="white",
                               font=("Helvetica Neue", 80, "bold"))
            canvas.pack()
            self.avatar_lbl = None

        if self.avatar_lbl:
            self.avatar_lbl.pack()

        # ── Indicador de estado ──────────────────────────────────
        self.estado_var = tk.StringVar(value="Di  'Martina'  para activarme")
        self.estado_lbl = tk.Label(
            self.root,
            textvariable=self.estado_var,
            font=("Helvetica Neue", 11),
            bg=BG_COLOR, fg=ACCENT_COLOR,
            pady=4
        )
        self.estado_lbl.pack()

        # ── Burbuja de texto ─────────────────────────────────────
        burbuja_frame = tk.Frame(self.root, bg=CARD_COLOR,
                                 padx=16, pady=12,
                                 relief=tk.FLAT, bd=0)
        burbuja_frame.pack(fill=tk.X, padx=24, pady=(4, 8))

        self.texto_var = tk.StringVar(value="Esperando activación...")
        self.texto_lbl = tk.Label(
            burbuja_frame,
            textvariable=self.texto_var,
            font=("Helvetica Neue", 11),
            bg=CARD_COLOR, fg=TEXT_COLOR,
            wraplength=400, justify=tk.LEFT,
            anchor="w"
        )
        self.texto_lbl.pack(fill=tk.X)

        # ── Panel inferior de opciones ───────────────────────────
        bottom = tk.Frame(self.root, bg=BOT_COLOR, pady=10)
        bottom.pack(fill=tk.X, side=tk.BOTTOM)

        # Toggle mostrar texto
        toggle_frame = tk.Frame(bottom, bg=BOT_COLOR)
        toggle_frame.pack(side=tk.LEFT, padx=16)

        tk.Label(
            toggle_frame, text="Mostrar texto",
            font=("Helvetica Neue", 9),
            bg=BOT_COLOR, fg="#A0B4C8"
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Checkbutton(
            toggle_frame,
            variable=self.mostrar_texto_var,
            bg=BOT_COLOR,
            activebackground=BOT_COLOR,
            selectcolor=ACCENT_COLOR,
            relief=tk.FLAT
        ).pack(side=tk.LEFT)

        # Toggle modo música: descarga vs YouTube
        self.modo_youtube_var = tk.BooleanVar(value=True)
        tk.Label(
            toggle_frame, text="   YouTube",
            font=("Helvetica Neue", 9),
            bg=BOT_COLOR, fg="#A0B4C8"
        ).pack(side=tk.LEFT, padx=(12, 4))
        tk.Checkbutton(
            toggle_frame,
            variable=self.modo_youtube_var,
            bg=BOT_COLOR,
            activebackground=BOT_COLOR,
            selectcolor=ACCENT_COLOR,
            relief=tk.FLAT
        ).pack(side=tk.LEFT)

        # Botón de salida
        tk.Button(
            bottom, text="Salir",
            font=("Helvetica Neue", 9),
            bg="#C0392B", fg="white",
            relief=tk.FLAT, padx=12, pady=4,
            command=self._salir
        ).pack(side=tk.RIGHT, padx=16)

        # ── Barra de estado de música ────────────────────────────
        self.musica_frame = tk.Frame(self.root, bg="#0A1520", pady=6)
        self.musica_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.musica_var = tk.StringVar(value="")
        self.musica_lbl = tk.Label(
            self.musica_frame,
            textvariable=self.musica_var,
            font=("Helvetica Neue", 9),
            bg="#0A1520", fg="#FAC775",
            wraplength=440
        )
        self.musica_lbl.pack()
        # Inicialmente oculta
        self.musica_frame.pack_forget()

        # ── Créditos ─────────────────────────────────────────────
        tk.Label(
            self.root,
            text="© 2025 Alfredo Díaz Claro — CDT Smart Regions Center — UNAB",
            font=("Helvetica Neue", 7),
            bg=BG_COLOR, fg="#4A6070"
        ).pack(side=tk.BOTTOM, pady=(0, 2))

    # ── Control del avatar ────────────────────────────────────────

    def _set_avatar(self, abierta: bool):
        if not self.avatar_lbl:
            return
        img = self.img_open if abierta else self.img_closed
        if img:
            self.avatar_lbl.config(image=img)
            self.avatar_lbl.image = img

    def _animar_boca(self, duracion_seg: float):
        """Alterna boca abierta/cerrada durante 'duracion_seg' segundos."""
        t0 = time.time()
        intervalo = 0.22  # segundos por frame
        abierta = True
        while time.time() - t0 < duracion_seg:
            self.root.after(0, self._set_avatar, abierta)
            abierta = not abierta
            time.sleep(intervalo)
        self.root.after(0, self._set_avatar, False)

    # ── TTS con sincronización ────────────────────────────────────

    def hablar(self, texto: str, mostrar=True):
        """Convierte texto a voz y sincroniza el avatar."""
        if not texto:
            return

        if self.mostrar_texto_var.get() and mostrar:
            self.root.after(0, self.texto_var.set, f"Martina: {texto}")

        # Estimar duración (145 palabras/min)
        num_palabras = len(texto.split())
        duracion = max(1.5, (num_palabras / 145) * 60)

        self.hablando = True
        self.root.after(0, self.estado_var.set, "Hablando...")

        hilo_anim = threading.Thread(
            target=self._animar_boca, args=(duracion,), daemon=True
        )
        hilo_anim.start()

        with self._tts_lock:
            engine.say(texto)
            engine.runAndWait()

        hilo_anim.join()
        self.hablando = False
        self.root.after(0, self._set_avatar, False)
        self.root.after(0, self.estado_var.set, "Di  'Martina'  para activarme")

    # ── STT ───────────────────────────────────────────────────────

    def _calibrar_microfono(self):
        """
        Calibra el micrófono UNA sola vez al iniciar.
        Evita el retardo de 0.4s en cada escucha.
        """
        r_cal = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r_cal.adjust_for_ambient_noise(source, duration=1.0)
                self._energy_threshold = r_cal.energy_threshold
                print(f"[MIC] Calibrado. Umbral de energía: {self._energy_threshold:.0f}")
        except Exception:
            self._energy_threshold = 300

    def escuchar(self, timeout_espera=5, phrase_limit=6) -> str:
        """
        Captura audio y devuelve el texto reconocido.
        Usa el umbral calibrado al inicio para respuesta inmediata.
        """
        r = sr.Recognizer()
        # Usar el umbral ya calibrado — sin adjust_for_ambient_noise aquí
        r.energy_threshold       = getattr(self, '_energy_threshold', 300)
        r.dynamic_energy_threshold = False   # No recalibrar en cada escucha
        r.pause_threshold        = 0.6       # Detecta fin de frase más rápido
        r.non_speaking_duration  = 0.4       # Margen antes de cortar

        try:
            with sr.Microphone() as source:
                self.root.after(0, self.estado_var.set, "Escuchando...")
                self.root.after(0, self._set_avatar, False)

                if self.mostrar_texto_var.get():
                    self.root.after(0, self.texto_var.set, "🎙️ Escuchando...")

                audio = r.listen(
                    source,
                    timeout=timeout_espera,
                    phrase_time_limit=phrase_limit
                )

            self.root.after(0, self.estado_var.set, "Procesando...")
            texto = r.recognize_google(audio, language='es-CO')
            print(f"[STT] Reconocido: {texto}")

            if self.mostrar_texto_var.get():
                self.root.after(0, self.texto_var.set, f"Tú: {texto}")

            return texto.lower().strip()

        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        except Exception as e:
            print(f"[STT Error] {e}")
            return ""

    # ── Saludo según hora ─────────────────────────────────────────

    def saludo_hora(self) -> str:
        hora = datetime.datetime.now().hour
        if 0 <= hora < 12:
            return "Buenos días"
        elif 12 <= hora < 18:
            return "Buenas tardes"
        else:
            return "Buenas noches"

    # ── Lógica de respuesta ───────────────────────────────────────

    def procesar_comando(self, query: str):
        """Determina la respuesta al comando del usuario."""
        q = query.lower()

        # ── Wikipedia ───────────────────────────────────────────
        if 'wikipedia' in q:
            tema = re.sub(r'(busca|en|wikipedia|sobre)', '', q).strip()
            if not tema:
                self.hablar("¿Qué tema buscamos en Wikipedia?")
                tema = self.escuchar()
            try:
                res = wikipedia.summary(tema, sentences=2)
                self.hablar(f"Según Wikipedia: {res}")
            except Exception:
                self.hablar("No encontré ese tema en Wikipedia.")

        # ── YouTube ──────────────────────────────────────────────
        elif 'youtube' in q:
            self.hablar("Abriendo YouTube.")
            webbrowser.open("https://youtube.com")

        # ── Google ───────────────────────────────────────────────
        elif 'google' in q and 'busca' not in q:
            self.hablar("Abriendo Google.")
            webbrowser.open("https://google.com")

        # ── Página web del CDT ───────────────────────────────────
        elif 'página' in q and ('laboratorio' in q or 'cdt' in q or 'smart' in q):
            self.hablar("Abriendo la página del Smart Regions Center.")
            webbrowser.open("https://smartregionscenter.com.co")

        # ── Mapa / Ubicación ─────────────────────────────────────
        elif any(p in q for p in ['dónde', 'donde', 'ubic', 'mapa', 'queda el laboratorio']):
            self.hablar(
                "El laboratorio está en la Avenida 42 número 48 guion 11, "
                "en Bucaramanga. Te abro el mapa."
            )
            webbrowser.open(
                "https://www.google.nl/maps/search/unab/@7.1170986,-73.1060737,17z"
            )

        # ── Fecha y hora ─────────────────────────────────────────
        elif any(p in q for p in ['fecha', 'hora', 'día de hoy', 'qué día']):
            ahora = datetime.datetime.now()
            self.hablar(
                f"Hoy es {ahora.strftime('%A %d de %B de %Y')} "
                f"y son las {ahora.strftime('%H horas con %M minutos')}."
            )

        # ── Clima ────────────────────────────────────────────────
        elif 'clima' in q or 'temperatura' in q or 'lluvia' in q:
            self.hablar("¿De qué ciudad quieres saber el clima?")
            ciudad = self.escuchar(phrase_limit=4)
            if ciudad:
                self._consultar_clima(ciudad)
            else:
                self.hablar("No escuché la ciudad, intenta de nuevo.")

        # ── Chiste ───────────────────────────────────────────────
        elif 'chiste' in q:
            self.hablar("Mis chistes son muy técnicos, pero escucha este:")
            self.hablar(pyjokes.get_joke(language='es', category='all'))

        # ── Música en streaming ──────────────────────────────────
        elif any(p in q for p in [
            'música', 'canción', 'canciones', 'pon ', 'toca ', 'reproduce',
            'salsa', 'vallenato', 'cumbia', 'rock', 'jazz', 'balada',
            'relajante', 'reggaeton', 'pausa', 'reanuda', 'siguiente canción',
            'detén la música', 'para la música', 'apaga la música'
        ]):
            self._gestionar_musica(q)

        # ── Email al director ────────────────────────────────────
        elif 'email' in q or 'correo' in q:
            self.hablar("¿Qué mensaje quieres enviar?")
            contenido = self.escuchar()
            if contenido:
                try:
                    self._enviar_email("adiaz@unab.edu.co", contenido)
                    self.hablar("El correo fue enviado correctamente.")
                except Exception:
                    self.hablar("No pude enviar el correo, intenta más tarde.")

        # ── Quién te creó ────────────────────────────────────────
        elif any(p in q for p in ['creó', 'creo', 'creaste', 'quién te hizo', 'naciste']):
            self.hablar(
                "Fui creada por Alfredo Díaz Claro, del Centro de Desarrollo "
                "Tecnológico Smart Regions Center de la UNAB. "
                "Aún soy joven y aprendo cada día."
            )

        # ── Nombre propio ────────────────────────────────────────
        elif any(p in q for p in ['tu nombre', 'cómo te llamas', 'quién eres']):
            self.hablar(
                f"Me llamo {ASSISTANT_NAME}. Soy la asistente virtual "
                "del Smart Regions Center."
            )

        # ── Amor / preguntas personales ──────────────────────────
        elif 'te amo' in q or 'novia' in q or 'novio' in q:
            self.hablar(
                "Agradezco el gesto, pero soy una inteligencia artificial. "
                "Mejor hablemos de tecnología o del CDT."
            )

        # ── Salud del asistente ──────────────────────────────────
        elif 'cómo estás' in q or 'qué tal estás' in q:
            self.hablar(
                "Muy bien, gracias por preguntar. "
                "Lista para ayudarte con lo que necesites."
            )

        # ── Hola ─────────────────────────────────────────────────
        elif any(p in q for p in ['hola', 'buenas', 'buenos días', 'buenas tardes']):
            self.hablar(
                f"{self.saludo_hora()}. Soy {ASSISTANT_NAME}, "
                "¿en qué puedo ayudarte hoy?"
            )

        # ── Nota ─────────────────────────────────────────────────
        elif 'nota' in q and ('escrib' in q or 'tom' in q or 'guard' in q):
            self.hablar("¿Qué quieres que anote?")
            contenido = self.escuchar()
            if contenido:
                with open("nota_martina.txt", "a", encoding="utf-8") as f:
                    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    f.write(f"[{ts}] {contenido}\n")
                self.hablar("Nota guardada correctamente.")

        # ── Salir ────────────────────────────────────────────────
        elif any(p in q for p in ['salir', 'chao', 'adiós', 'adios', 'apagar', 'terminar']):
            self.hablar("Gracias por visitarnos. ¡Hasta pronto!")
            self.root.after(1500, self._salir)

        # ── Base de conocimiento CDT (siempre se intenta antes del fallback)
        else:
            # 1. Buscar primero en el diccionario del CDT
            respuesta_cdt = buscar_en_conocimiento(q)
            if respuesta_cdt:
                self.hablar(respuesta_cdt)
            else:
                # 2. Si no hay match en el CDT, intentar con LLaMA
                respuesta_llama = self._consultar_llama(q)
                if respuesta_llama:
                    self.hablar(respuesta_llama)
                else:
                    self.hablar(
                        "No tengo información sobre eso. "
                        "Puedes preguntarme sobre misión, servicios, sectores, "
                        "aliados, contacto, turismo, energía, formación, "
                        "convocatorias o cualquier tema del Smart Regions Center."
                    )

    # ── Barra de estado de música ─────────────────────────────────

    def _mostrar_estado_musica(self, texto: str):
        """Muestra la barra de estado de música con un mensaje."""
        self.musica_var.set(texto)
        self.root.after(0, self.musica_frame.pack,
                        {"fill": tk.X, "side": tk.BOTTOM, "before": self.estado_lbl})

    def _ocultar_estado_musica(self):
        """Oculta la barra de estado de música."""
        self.musica_var.set("")
        self.root.after(0, self.musica_frame.pack_forget)

    # ── Gestión de música ─────────────────────────────────────────

    def _gestionar_musica(self, query: str):
        """
        Maneja todos los comandos de música.
        Modo YouTube: abre el navegador con la búsqueda → sin descarga.
        Modo descarga: usa yt-dlp + pygame → reproduce internamente.
        """
        q = query.lower()

        if not MUSICA_DISPONIBLE and not self.modo_youtube_var.get():
            self.hablar(
                "El módulo de música no está disponible. "
                "Activa el modo YouTube en la pantalla para escuchar música."
            )
            return

        if self.player_musica:
            self.player_musica._hablar = self.hablar

        # ── Comandos de control (pausar, detener, siguiente) ──────
        comandos_control = [
            'pausa', 'pausar', 'para la música', 'silencia',
            'reanuda', 'continúa', 'sigue', 'siguiente', 'otra canción',
            'detén', 'apaga la música', 'stop música'
        ]
        if any(p in q for p in comandos_control) and self.player_musica:
            interpretar_comando_musica(q, self.player_musica)
            return

        # ── Determinar qué buscar ─────────────────────────────────
        busqueda = _extraer_busqueda(q) if MUSICA_DISPONIBLE else q

        # ── Modo YouTube (checkbox activo) ────────────────────────
        if self.modo_youtube_var.get():
            self._reproducir_youtube(busqueda)
            return

        # ── Modo descarga (checkbox inactivo) ─────────────────────
        if not MUSICA_DISPONIBLE:
            self.hablar("No tengo el módulo de música instalado.")
            return

        self.player_musica._hablar = self.hablar
        manejado = interpretar_comando_musica(q, self.player_musica)
        if not manejado:
            if busqueda:
                self._mostrar_estado_musica(
                    f"⬇ Descargando: {busqueda}  —  espera un momento..."
                )
                # Actualizar callback para mostrar título cuando esté listo
                def _cb(texto):
                    self.hablar(texto)
                    if texto.startswith("Reproduciendo:"):
                        self._mostrar_estado_musica(f"♪  {texto.replace('Reproduciendo: ', '')}")
                    elif texto.startswith("No pude"):
                        self._ocultar_estado_musica()
                self.player_musica._hablar = _cb
                self.player_musica.reproducir(busqueda)
            else:
                self.hablar("¿Qué música quieres escuchar?")

    def _reproducir_youtube(self, busqueda: str):
        """
        Abre YouTube en el navegador con la búsqueda.
        No descarga nada. El usuario controla el navegador.
        Martina sigue funcionando normalmente en paralelo.
        """
        import urllib.parse
        termino = urllib.parse.quote_plus(busqueda)
        url_busqueda = f"https://www.youtube.com/results?search_query={termino}"

        self.hablar(
            f"Abriendo YouTube con {busqueda}. "
            "Cuando quieras parar cierra el navegador y sigo contigo."
        )
        webbrowser.open(url_busqueda)
        self._mostrar_estado_musica(
            f"♪ YouTube abierto: {busqueda}  —  cierra el navegador para continuar"
        )

    # ── Consulta clima ────────────────────────────────────────────

    def _consultar_clima(self, ciudad: str):
        try:
            url = (
                f"http://api.openweathermap.org/data/2.5/weather"
                f"?appid={WEATHER_API_KEY}&q={ciudad}&lang=es"
            )
            r = requests.get(url, timeout=5)
            x = r.json()
            if x.get("cod") not in ("404", "400", 404, 400):
                temp = round(float(x["main"]["temp"]) - 273.15, 1)
                hum  = x["main"]["humidity"]
                desc = x["weather"][0]["description"]
                self.hablar(
                    f"En {ciudad} la temperatura es de {temp} grados, "
                    f"con {desc} y {hum} por ciento de humedad."
                )
            else:
                self.hablar("No encontré información para esa ciudad.")
        except Exception:
            self.hablar("No pude conectarme al servicio del clima.")

    # ── Consulta LLaMA (HuggingFace) ─────────────────────────────

    def _consultar_llama(self, pregunta: str) -> str:
        try:
            hf_url = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
            headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
            prompt  = (
                "Eres Martina, asistente del CDT Smart Regions Center. "
                "Responde en español de manera concisa y amable. "
                f"Pregunta: {pregunta}"
            )
            data = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            resp = requests.post(hf_url, headers=headers, json=data, timeout=15)
            if resp.status_code == 200:
                result = resp.json()
                if isinstance(result, list):
                    return result[0].get("generated_text", "").strip()
                return result.get("generated_text", "").strip()
        except Exception as e:
            print(f"[LLaMA Error] {e}")
        return ""

    # ── Email ─────────────────────────────────────────────────────

    def _enviar_email(self, destinatario: str, contenido: str):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('adiaz@unab.edu.co', 'EMAIL_PASSWORD')
        server.sendmail('adiaz@unab.edu.co', destinatario, contenido)
        server.close()

    # ── Motor principal de escucha ────────────────────────────────

    def _motor_principal(self):
        """Bucle principal: espera la palabra 'Martina' y activa el asistente."""
        time.sleep(1.5)  # Esperar a que la UI esté lista

        # Saludo inicial
        saludo = self.saludo_hora()
        self.hablar(
            f"{saludo}. Soy {ASSISTANT_NAME}, la asistente virtual "
            "del Smart Regions Center. "
            f"Di '{ASSISTANT_NAME}' cuando necesites ayuda."
        )

        # Esperar a que el micrófono esté calibrado
        time.sleep(0.5)

        r_wake = sr.Recognizer()
        r_wake.pause_threshold         = 0.5
        r_wake.non_speaking_duration   = 0.3
        r_wake.dynamic_energy_threshold = False

        while True:
            # Actualizar umbral desde la calibración inicial
            r_wake.energy_threshold = getattr(self, '_energy_threshold', 300)

            # No escuchar wake word mientras descarga música
            if (MUSICA_DISPONIBLE and
                    self.player_musica and
                    self.player_musica._descargando):
                time.sleep(0.3)
                continue

            try:
                with sr.Microphone() as source:
                    self.root.after(0, self.estado_var.set,
                                    f"Di  '{ASSISTANT_NAME}'  para activarme")
                    # Sin adjust_for_ambient_noise aquí — ya está calibrado
                    audio = r_wake.listen(
                        source, timeout=5, phrase_time_limit=3
                    )

                texto = r_wake.recognize_google(
                    audio, language='es-CO'
                ).lower()
                print(f"[WAKE] Detectado: {texto}")

                # Detección flexible de "martina"
                if any(w in texto for w in [
                    'martina', 'mar tina', 'máquina', 'marina', 'martín'
                ]):
                    self._ciclo_conversacion()

            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except sr.RequestError:
                time.sleep(2)
                continue
            except Exception as e:
                print(f"[WAKE Error] {e}")
                time.sleep(1)

    def _ciclo_conversacion(self):
        """Una vez activada, escucha y responde hasta que el usuario termine."""
        self.root.after(0, self.estado_var.set, "Activada")
        self.hablar("Dime, ¿en qué te puedo ayudar?", mostrar=False)

        turnos_silencio = 0
        MAX_SILENCIO    = 2  # Desactiva tras 2 silencios consecutivos

        while True:
            # ── Esperar si la música está descargando ─────────────
            # El STT captaría el audio del parlante como voz del usuario
            if (MUSICA_DISPONIBLE and
                    self.player_musica and
                    self.player_musica._descargando):
                self.root.after(0, self.estado_var.set, "Descargando música...")
                time.sleep(0.5)
                continue

            query = self.escuchar(timeout_espera=6, phrase_limit=8)

            if not query:
                turnos_silencio += 1
                if turnos_silencio >= MAX_SILENCIO:
                    self.hablar("Quedé en silencio. Di Martina cuando me necesites.")
                    break
                continue

            turnos_silencio = 0

            # Salir del ciclo
            if any(p in query for p in ['salir', 'chao', 'adiós', 'adios', 'apagar']):
                self.procesar_comando(query)
                break

            # Responder
            self.procesar_comando(query)

            # Después de responder, preguntar si necesita algo más
            # (solo si la música NO está sonando — evita interrumpirla)
            musica_activa = (MUSICA_DISPONIBLE and
                             self.player_musica and
                             self.player_musica.esta_reproduciendo())
            if not musica_activa:
                time.sleep(0.5)
                self.hablar("¿Hay algo más en lo que pueda ayudarte?", mostrar=False)

    # ── Salir ─────────────────────────────────────────────────────

    def _salir(self):
        self.root.destroy()


# ── Entry point ───────────────────────────────────────────────────

def main():
    root = tk.Tk()
    root.geometry("480x620")
    app  = MartinApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
