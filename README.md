# MARTINA — Asistente Virtual de Voz
## Smart Regions Center · CDT · UNAB

**Autor:** Alfredo Díaz Claro  
**Institución:** Centro de Desarrollo Tecnológico Smart Regions Center  
**Universidad:** Autónoma de Bucaramanga — UNAB  
**Contacto:** adiaz@unab.edu.co  
**Versión:** 2.0 — 2026

---

## ¿Qué es Martina?

Martina es un asistente de voz tipo Alexa especializado en información
del CDT Smart Regions Center. Tiene un avatar animado con sincronización
de labios, reconocimiento de voz en español colombiano, y responde
preguntas sobre el centro, servicios, proyectos y más.

---

## Versión de Python recomendada

> ✅ **Python 3.10.x — versión recomendada para este proyecto**

Esta es la versión con mejor compatibilidad garantizada para todas las
bibliotecas del proyecto, especialmente `PyAudio`, que es la más
exigente en cuanto a versión de Python.

### Tabla de compatibilidad verificada

| Biblioteca          | 3.8 | 3.9 | 3.10 ✅ | 3.11 | 3.12 | 3.13 |
|---------------------|-----|-----|---------|------|------|------|
| `pyttsx3`           | ✅  | ✅  | ✅      | ✅   | ✅   | ✅   |
| `SpeechRecognition` | ✅  | ✅  | ✅      | ✅   | ✅   | ✅   |
| `PyAudio 0.2.14`    | ✅  | ✅  | ✅      | ✅   | ✅   | ⚠️   |
| `Pillow 10.4`       | ✅  | ✅  | ✅      | ✅   | ✅   | ✅   |
| `requests`          | ✅  | ✅  | ✅      | ✅   | ✅   | ✅   |
| `wikipedia`         | ✅  | ✅  | ✅      | ✅   | ✅   | ✅   |
| `pyjokes`           | ✅  | ✅  | ✅      | ✅   | ✅   | ✅   |

⚠️ Python 3.13 puede fallar al instalar PyAudio por falta de compiladores
C++ en Windows, requiriendo pasos adicionales.

### ¿Por qué 3.10 y no una versión más nueva?

`PyAudio` tiene wheels (binarios precompilados) para Windows disponibles
desde la versión 3.8 hasta 3.12 sin necesidad de compiladores ni pasos
extra. Con **Python 3.10** el comando `pip install PyAudio` funciona
directamente, sin `pipwin`, sin Visual Studio Build Tools, sin archivos
`.whl` manuales.

### Cómo instalar Python 3.10

1. Descarga desde:
   **https://www.python.org/downloads/release/python-31011/**

2. Durante la instalación marca la casilla:
   ☑ **"Add Python 3.10 to PATH"**

3. Verifica la instalación:
   ```bash
   python --version
   # Debe mostrar: Python 3.10.x
   ```

---

## Estructura del proyecto

```
martina/
│
├── asistente_martina.py     ← Código principal
├── musica.py                ← Módulo de streaming de música
├── requirements.txt         ← Dependencias
├── .env                     ← Credenciales (NO se sube a GitHub)
├── .gitignore               ← Archivos excluidos de Git
├── README.md                ← Este archivo
├── nota_martina.txt         ← Se crea automáticamente al tomar notas
│
└── images/                  ← DEBES crear esta carpeta con tus avatares
    ├── bocaabiertaf.png     ← Avatar con boca abierta (hablando)
    └── bocacerradaf.png     ← Avatar con boca cerrada (en reposo)
```

---

## Instalación paso a paso

### 1. Crear entorno virtual

```bash
python -m venv env
```

### 2. Activar el entorno

```bash
# Windows
env\Scripts\activate.bat

# Linux / Mac
source env/bin/activate
```

### 3. Actualizar pip

```bash
python -m pip install --upgrade pip
```

### 4. Instalar PyAudio

Con **Python 3.10** esto funciona directamente sin pasos adicionales:

```bash
pip install PyAudio
```

Si usas Python 3.11 o 3.12 y falla, prueba:

```bash
pip install pipwin
pipwin install pyaudio
```

Si usas Python 3.13 y falla, descarga el wheel precompilado desde:
**https://pypi.org/project/PyAudio/#files**
y luego instálalo así:

```bash
pip install PyAudio-0.2.14-cp313-cp313-win_amd64.whl
```

### 5. Instalar el resto de dependencias

```bash
pip install -r requirements.txt
pip install python-dotenv
```

### 6. Configurar credenciales

Crea un archivo `.env` en la raíz del proyecto:

```
HF_API_TOKEN=tu_token_de_huggingface
WEATHER_API_KEY=tu_api_key_de_openweathermap
EMAIL_PASSWORD=tu_contraseña_de_aplicacion_gmail
```

---

## Carpeta de imágenes (avatares)

Crea la carpeta `images/` junto al archivo principal y coloca:

| Archivo             | Descripción                          |
|---------------------|--------------------------------------|
| `bocaabiertaf.png`  | Imagen con boca abierta (hablando)   |
| `bocacerradaf.png`  | Imagen con boca cerrada (en reposo)  |

Tamaño recomendado: **400×400 px** o más, fondo blanco o transparente.

Si no colocas imágenes, la interfaz mostrará un círculo de color
como avatar alternativo y funcionará igual.

---

## Cómo ejecutar

```bash
python asistente_martina.py
```

---

## Botón de texto (parte inferior de la pantalla)

En la parte inferior de la ventana hay un checkbox **"Mostrar texto"**:

- **Activado** → Aparece en pantalla el texto que reconoció el micrófono
  y el texto que va a decir Martina.
- **Desactivado** → Solo se escucha la voz, sin texto visible.

---

## Cómo funciona la detección de "Martina"

El sistema funciona en dos capas, igual que Alexa:

1. **Escucha pasiva**: El micrófono monitorea continuamente buscando
   solo la palabra "Martina". Consume muy poca CPU.

2. **Ciclo activo**: Al detectar "Martina", el sistema se activa y
   escucha comandos completos hasta que el usuario dice "chao" o
   hay 2 silencios consecutivos.

El reconocimiento acepta variaciones fonéticas como "Mar tina",
"marina", etc., para reducir errores de pronunciación.

---

## Mejoras aplicadas respecto al código original

| Problema original                         | Solución aplicada                                     |
|-------------------------------------------|-------------------------------------------------------|
| `pygame` para UI (limitado)              | `tkinter` con diseño moderno                          |
| Nombre "Smartina" sonaba en inglés       | Cambiado a "Martina" con detección fonética flexible  |
| Animación bloqueaba el hilo principal    | Avatar corre en hilo separado con `threading`         |
| `takeCommand2()` sin timeout controlado  | `sr.WaitTimeoutError` manejado correctamente          |
| TTS bloqueaba la interfaz                | Lock (`_tts_lock`) + hilo de animación independiente  |
| Base de conocimiento en `elif` repetidos | Diccionario `CONOCIMIENTO_CDT` con búsqueda por score |
| Credenciales en texto plano              | Archivo `.env` separado, excluido de Git              |
| Sin opción de mostrar/ocultar texto      | Checkbox en panel inferior                            |
| Sin créditos visibles                    | Footer con crédito al autor en la interfaz            |
| Importaciones innecesarias (`winshell`)  | Solo se importa lo necesario y multiplataforma        |
| Música solo desde carpeta local          | Streaming gratuito vía yt-dlp + YouTube               |
| Calibración de micrófono en cada escucha | Calibración única al inicio, respuesta inmediata      |

---

## Recomendaciones para mejorar la naturalidad

1. **Python 3.10**: Usa esta versión para evitar problemas de
   compatibilidad con PyAudio en Windows. Es la más estable para
   este stack de bibliotecas.

2. **Micrófono**: Usa un micrófono USB o de diadema. Los micrófonos
   integrados del laptop capturan mucho ruido y el reconocimiento
   empeora notablemente.

3. **Voz TTS**: En Windows instala voces adicionales en español desde
   Configuración → Hora e idioma → Idioma → Español Colombia →
   Síntesis de voz. Las voces "Sabina" o "Helena" suenan más naturales.

4. **Velocidad de respuesta**: El parámetro `rate=145` es ideal para
   español. Puedes bajar a `135` para una voz más pausada y clara.

5. **Imágenes del avatar**: Mientras más diferencia visual haya entre
   `bocaabiertaf.png` y `bocacerradaf.png`, más vivo se verá el efecto
   de sincronización.

6. **Base de conocimiento**: Puedes ampliar el diccionario
   `CONOCIMIENTO_CDT` en el código con más preguntas y respuestas
   específicas del CDT sin necesidad de cambiar la lógica.

7. **Idioma STT**: Se configuró `es-CO` (español Colombia) en lugar de
   `es-ES` para mejorar el reconocimiento del acento santandereano.

---

## Solución de problemas comunes

| Error                               | Solución                                                        |
|-------------------------------------|-----------------------------------------------------------------|
| `No module named 'pyaudio'`        | Usar Python 3.10 y ejecutar `pip install PyAudio`               |
| PyAudio falla en Python 3.13       | Descargar wheel desde pypi.org/project/PyAudio/#files           |
| `OSError: [WinError 2]` en pyttsx3 | Instalar voces en español en Windows (ver recomendación 3)      |
| Avatar no aparece                  | Verificar que `images/` existe con las dos imágenes             |
| No reconoce "Martina"              | Hablar más cerca del micrófono, en ambiente silencioso          |
| TTS habla muy rápido               | Cambiar `rate=145` a un valor menor como `130`                  |
| `python --version` muestra 3.13    | Instalar Python 3.10 desde python.org y crear el entorno con él |
| GitHub rechaza el push             | Mover credenciales al archivo `.env` y repetir el push          |

---

## Guía de preguntas por categoría

Esta sección muestra exactamente qué decirle a Martina en cada situación.
Primero actívala diciendo **"Martina"** y luego hace tu pregunta.

---

### Activación y saludo

```
"Martina"
"Martina, ¿estás ahí?"
"Martina, necesito ayuda"
```

---

### Información general del CDT Smart Regions Center

```
"¿Qué es el CDT?"
"¿Qué es el Smart Regions Center?"
"Cuéntame sobre el centro"
"¿A qué universidad pertenece el centro?"
"¿Cuándo inició el proyecto?"
"¿Quién conforma el Smart Regions Center?"
"¿Cómo se articula el centro con la sociedad?"
"¿Qué son los territorios inteligentes?"
```

---

### Misión, visión y objetivos

```
"¿Cuál es la misión del CDT?"
"¿Cuál es la visión del centro?"
"¿Cuál es el objetivo del laboratorio?"
"¿Para qué fue creado el Smart Regions Center?"
"¿Qué busca lograr el CDT en Santander?"
```

---

### Servicios y tecnologías

```
"¿Qué servicios ofrece el CDT?"
"¿Qué tecnologías maneja el laboratorio?"
"¿Qué es la vigilancia tecnológica?"
"¿El centro hace prototipado?"
"¿Qué es la maduración de tecnologías?"
"¿Desarrollan soluciones IoT?"
"¿Trabajan con inteligencia artificial?"
"¿Qué temas cubre el laboratorio?"
"¿Qué es el acompañamiento en implantación de tecnología?"
```

---

### Sectores estratégicos

```
"¿En qué sectores trabaja el CDT?"
"¿Qué sectores tiene el laboratorio?"
"¿Tienen proyectos en salud?"
"¿Cómo apoyan el turismo?"
"¿Trabajan en biodiversidad?"
"¿Qué hacen en el sector energía?"
"¿Tienen proyectos de agroindustria?"
"¿Qué hacen en manufactura?"
```

---

### Proyectos específicos

```
"¿Qué es el proyecto Conexión Natural?"
"¿Qué proyectos tienen en Río de Oro?"
"¿En qué consiste la plataforma de energía P2P?"
"¿Qué es el monitoreo de biofertilizantes?"
"¿Tienen casos de éxito documentados?"
"¿Qué han hecho con Penagos Hermanos?"
```

---

### Aliados y colaboraciones

```
"¿Quiénes son los aliados del CDT?"
"¿Qué es UNIRED?"
"¿Qué hace Phina Biosoluciones?"
"¿Trabajan con MinCiencias?"
"¿Cómo se financió el centro?"
"¿De dónde vienen los recursos del CDT?"
```

---

### Formación y talento humano

```
"¿El centro da entrenamiento?"
"¿Cómo apoya el CDT al talento humano?"
"¿Tienen semilleros de investigación?"
"¿Hay oportunidades de formación?"
"¿Cómo instalan capacidades en la región?"
```

---

### Contacto y ubicación

```
"¿Dónde queda el laboratorio?"
"¿Dónde están ubicados?"
"¿Cuál es el teléfono del CDT?"
"¿Cuál es el correo del centro?"
"¿Cuál es la página web del Smart Regions Center?"
"¿Cómo me suscribo para recibir noticias?"
"¿Dónde están las convocatorias?"
"¿Cómo puedo aplicar a una vacante?"
```

---

### El laboratorio Smart Center Lab

```
"¿Qué es el Smart Center Lab?"
"¿Qué áreas tiene el laboratorio?"
"¿Qué se hace en el área de ideación?"
"¿Qué es el área de prototipado?"
"¿Tienen área de manufactura?"
```

---

### Clima

```
"¿Cómo está el clima en Bucaramanga?"
"¿Cómo está la temperatura en Medellín?"
"¿Está lloviendo en Bogotá?"
"¿Cuál es la temperatura en Cali?"
"¿Cómo está el clima en Barranquilla?"
```

---

### Fecha y hora

```
"¿Qué hora es?"
"¿Qué fecha es hoy?"
"¿Qué día es hoy?"
"¿Cuál es la fecha y hora actual?"
```

---

### Música en streaming (sin costo, sin descarga)

```
"Pon música"
"Toca salsa"
"Pon vallenato"
"Toca cumbia colombiana"
"Quiero escuchar música relajante"
"Pon música para trabajar"
"Toca música para estudiar"
"Pon a Carlos Vives"
"Toca a Shakira"
"Pon jazz"
"Toca rock en español"
"Quiero reggaeton"
"Pon baladas románticas"
"Pausa la música"
"Reanuda la música"
"Siguiente canción"
"Apaga la música"
"Para la música"
```

---

### Búsqueda en Wikipedia

```
"Busca en Wikipedia inteligencia artificial"
"Busca en Wikipedia Internet de las Cosas"
"¿Qué dice Wikipedia sobre la UNAB?"
"Busca en Wikipedia Bucaramanga"
"Wikipedia Internet de las Cosas"
```

---

### Navegación web

```
"Abre YouTube"
"Abre Google"
"Abre la página del laboratorio"
"Muéstrame la página del CDT"
"¿Dónde queda el laboratorio?" → (abre Google Maps automáticamente)
```

---

### Notas de voz

```
"Toma una nota"
"Escribe una nota"
"Guarda una nota"
```
*(Martina te pide que dictes el contenido)*

---

### Correo electrónico

```
"Envía un correo al director"
"Manda un email"
"Envía un correo"
```
*(Martina te pide el mensaje a dictar)*

---

### Chistes

```
"Cuéntame un chiste"
"Dime un chiste"
"Quiero escuchar un chiste"
```

---

### Conversación general

```
"Hola Martina"
"¿Cómo estás?"
"¿Quién eres?"
"¿Cómo te llamas?"
"¿Quién te creó?"
"¿Para qué te crearon?"
"¿Quién te hizo?"
"Te amo" → (respuesta educada)
"¿Qué es el amor?"
```

---

### Cerrar o desactivar

```
"Chao"
"Adiós"
"Salir"
"Apagar"
"Terminar"
```

---

## Créditos

```
╔═══════════════════════════════════════════════════════════╗
║  Martina — Asistente Virtual con Voz y Avatar             ║
║                                                           ║
║  Autor:       Alfredo Díaz Claro                          ║
║  Institución: CDT Smart Regions Center — UNAB             ║
║  Email:       adiaz@unab.edu.co                           ║
║  Web:         smartregionscenter.com.co                   ║
║  Versión:     2.0 — 2026                                  ║
╚═══════════════════════════════════════════════════════════╝
```
