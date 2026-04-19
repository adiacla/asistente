"""
╔══════════════════════════════════════════════════════════════════╗
║          MARTINA - Módulo de Música en Streaming                 ║
║          Smart Regions Center - CDT UNAB                        ║
║                                                                  ║
║  Autor: Alfredo Díaz Claro — adiaz@unab.edu.co                  ║
║  Versión: 2.0 | 2026                                             ║
╚══════════════════════════════════════════════════════════════════╝

Descripción:
    Módulo de reproducción de música en streaming gratuito.
    Usa yt-dlp para buscar en YouTube y obtener la URL de audio
    directamente, luego pygame la reproduce sin descargar el archivo.

    No requiere API key. 100% gratuito y legal para uso personal.

Dependencias adicionales:
    pip install yt-dlp pygame

Uso desde el asistente:
    from musica import PlayerMusica
    player = PlayerMusica(callback_hablar=self.hablar)
    player.reproducir("salsa colombiana")
    player.pausar()
    player.reanudar()
    player.detener()
    player.siguiente()
"""

import threading
import time
import os
import re
import tempfile
import pygame

try:
    import yt_dlp
    YT_DLP_DISPONIBLE = True
except ImportError:
    YT_DLP_DISPONIBLE = False


# ── Configuración del player ──────────────────────────────────────

CARPETA_CACHE = os.path.join(tempfile.gettempdir(), "martina_musica")
os.makedirs(CARPETA_CACHE, exist_ok=True)

# Géneros y búsquedas sugeridas en español
GENEROS_SUGERIDOS = {
    'salsa'       : 'salsa colombiana mix',
    'vallenato'   : 'vallenato clásico mix',
    'cumbia'      : 'cumbia colombiana mix',
    'relajante'   : 'música relajante instrumental',
    'rock'        : 'rock en español clásicos',
    'pop'         : 'pop latino mix 2024',
    'reggaeton'   : 'reggaeton mix 2024',
    'clásica'     : 'música clásica instrumental relajante',
    'jazz'        : 'jazz instrumental suave',
    'tropical'    : 'música tropical colombiana',
    'electrónica' : 'música electrónica instrumental',
    'balada'      : 'baladas románticas en español',
    'navidad'     : 'villancicos navideños colombianos',
    'trabajo'     : 'música para trabajar concentración',
    'estudio'     : 'música para estudiar concentración',
}


class PlayerMusica:
    """
    Reproductor de música en streaming usando yt-dlp + pygame.
    No requiere ninguna API key.
    """

    def __init__(self, callback_hablar=None):
        """
        Args:
            callback_hablar: Función del asistente para hablar (speak).
                             Si es None, usa print().
        """
        self._hablar = callback_hablar or print
        self._reproduciendo = False
        self._pausado = False
        self._descargando = False   # True mientras descarga → bloquea el STT
        self._hilo = None
        self._archivo_actual = None
        self._titulo_actual  = ""
        self._cola = []          # Cola de canciones pendientes
        self._lock = threading.Lock()

        # Inicializar pygame mixer si no está inicializado
        if not pygame.get_init():
            pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

    # ── API pública ───────────────────────────────────────────────

    def reproducir(self, busqueda: str) -> bool:
        """
        Busca la canción o género en YouTube y la reproduce en streaming.

        Args:
            busqueda: Texto de búsqueda (artista, canción, género, etc.)

        Returns:
            True si inició la reproducción, False si hubo error.
        """
        if not YT_DLP_DISPONIBLE:
            self._hablar(
                "No tengo instalado el módulo de música. "
                "Pídele al administrador que instale yt-dlp."
            )
            return False

        # Resolver alias de género
        busqueda_efectiva = self._resolver_genero(busqueda)

        self._hablar(f"Buscando {busqueda_efectiva}... dame un momento.")
        self.detener()  # Detener lo que suene actualmente

        self._hilo = threading.Thread(
            target=self._ciclo_reproduccion,
            args=(busqueda_efectiva,),
            daemon=True
        )
        self._hilo.start()
        return True

    def detener(self):
        """Detiene la reproducción actual."""
        self._reproduciendo = False
        self._pausado = False
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass
        self._limpiar_cache()

    def pausar(self):
        """Pausa o reanuda la reproducción."""
        if not pygame.mixer.get_init():
            return
        if self._pausado:
            pygame.mixer.music.unpause()
            self._pausado = False
            self._hablar("Música reanudada.")
        else:
            pygame.mixer.music.pause()
            self._pausado = True
            self._hablar("Música pausada.")

    def reanudar(self):
        """Reanuda si está pausado."""
        if self._pausado:
            pygame.mixer.music.unpause()
            self._pausado = False
            self._hablar("Reanudando la música.")

    def siguiente(self):
        """Pasa a la siguiente canción de la cola."""
        if self._cola:
            self._hablar("Pasando a la siguiente canción.")
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        else:
            self._hablar("No hay más canciones en la cola.")

    def esta_reproduciendo(self) -> bool:
        return self._reproduciendo and not self._pausado

    def titulo_actual(self) -> str:
        return self._titulo_actual

    # ── Lógica interna ────────────────────────────────────────────

    def _resolver_genero(self, texto: str) -> str:
        """Convierte alias de géneros a búsquedas más efectivas."""
        texto_lower = texto.lower().strip()
        for alias, busqueda in GENEROS_SUGERIDOS.items():
            if alias in texto_lower:
                return busqueda
        return texto

    def _ciclo_reproduccion(self, busqueda: str):
        """Descarga y reproduce canciones en bucle desde YouTube."""
        self._reproduciendo = True
        intentos_fallidos  = 0
        MAX_INTENTOS       = 3

        while self._reproduciendo and intentos_fallidos < MAX_INTENTOS:
            url_audio, titulo = self._obtener_url_audio(busqueda)

            if not url_audio:
                intentos_fallidos += 1
                if intentos_fallidos >= MAX_INTENTOS:
                    self._hablar(
                        "No pude conectarme al servicio de música. "
                        "Verifica tu conexión a internet."
                    )
                    break
                time.sleep(2)
                continue

            intentos_fallidos = 0
            self._titulo_actual = titulo
            self._hablar(f"Reproduciendo: {titulo}")

            exito = self._reproducir_url(url_audio)
            if not exito:
                intentos_fallidos += 1

        self._reproduciendo = False

    def _obtener_url_audio(self, busqueda: str):
        """
        Usa yt-dlp para buscar en YouTube y obtener la URL de audio
        directamente (sin descargar el archivo completo).

        Returns:
            Tupla (url_audio, titulo) o (None, None) si falla.
        """
        opciones_ydl = {
            'format'          : 'bestaudio/best',
            'quiet'           : True,
            'no_warnings'     : True,
            'extract_flat'    : False,
            'noplaylist'      : True,
            # Obtener solo la URL, no descargar
            'skip_download'   : True,
            # Límite de resultados de búsqueda
            'default_search'  : 'ytsearch1',
        }

        try:
            with yt_dlp.YoutubeDL(opciones_ydl) as ydl:
                info = ydl.extract_info(
                    f"ytsearch1:{busqueda}",
                    download=False
                )

                if not info:
                    return None, None

                # Extraer el primer resultado
                if 'entries' in info:
                    entrada = info['entries'][0]
                else:
                    entrada = info

                titulo = entrada.get('title', 'Canción desconocida')

                # Obtener la URL del mejor formato de audio
                formatos = entrada.get('formats', [])
                url_audio = None

                # Buscar formato de solo audio (más eficiente para streaming)
                for fmt in reversed(formatos):
                    if (fmt.get('acodec') != 'none' and
                            fmt.get('vcodec') == 'none' and
                            fmt.get('url')):
                        url_audio = fmt['url']
                        break

                # Si no hay formato solo-audio, usar el mejor disponible
                if not url_audio:
                    url_audio = entrada.get('url')

                return url_audio, titulo

        except Exception as e:
            print(f"[Música Error] {e}")
            return None, None

    def _reproducir_url(self, url: str) -> bool:
        """
        Descarga el audio en un archivo temporal y lo reproduce con pygame.
        Usa calidad baja (64kbps, máx 8MB) para descarga en segundos.

        Returns:
            True si la reproducción fue exitosa.
        """
        archivo_temp = os.path.join(
            CARPETA_CACHE, f"martina_{int(time.time())}"
        )

        # ── Opciones de descarga optimizadas para velocidad ───────
        # worstaudio = formato más liviano disponible (~1-3MB típico)
        # Sin FFmpeg postprocessing = sin conversión = más rápido
        # match_filter limita a videos cortos (evita descargar álbumes de 1h)
        opciones_descarga = {
            'format'         : 'worstaudio/worst',   # Calidad mínima → descarga rápida
            'quiet'          : True,
            'no_warnings'    : True,
            'noplaylist'     : True,
            'outtmpl'        : archivo_temp + '.%(ext)s',
            # Abortar si el archivo supera 15MB (evita videos larguísimos)
            'max_filesize'   : 15 * 1024 * 1024,
            # Preferir videos cortos (menos de 10 minutos)
            'match_filter'   : yt_dlp.utils.match_filter_func(
                                   'duration < 600'
                               ),
        }

        self._descargando = True
        print(f"[Música] Descargando audio liviano para: {self._titulo_actual}")

        try:
            with yt_dlp.YoutubeDL(opciones_descarga) as ydl:
                ydl.download([url])

            self._descargando = False

            # Buscar el archivo descargado en la carpeta de cache
            archivo_real = None
            for f in os.listdir(CARPETA_CACHE):
                ruta = os.path.join(CARPETA_CACHE, f)
                if os.path.isfile(ruta):
                    archivo_real = ruta
                    break

            if not archivo_real:
                print("[Música] No se encontró el archivo descargado.")
                return False

            self._archivo_actual = archivo_real
            tam_mb = os.path.getsize(archivo_real) / (1024 * 1024)
            print(f"[Música] Descargado: {os.path.basename(archivo_real)} ({tam_mb:.1f} MB)")

            # Reproducir con pygame
            pygame.mixer.music.load(archivo_real)
            pygame.mixer.music.set_volume(0.75)
            pygame.mixer.music.play()

            # Esperar a que termine o sea interrumpido
            while pygame.mixer.music.get_busy() and self._reproduciendo:
                if self._pausado:
                    time.sleep(0.1)
                    continue
                time.sleep(0.5)

            pygame.mixer.music.stop()
            return True

        except Exception as e:
            print(f"[Música Reproducción Error] {e}")
            return False

        finally:
            self._descargando = False
            self._limpiar_cache()

    def _limpiar_cache(self):
        """Elimina archivos temporales de música."""
        try:
            for f in os.listdir(CARPETA_CACHE):
                ruta = os.path.join(CARPETA_CACHE, f)
                try:
                    os.remove(ruta)
                except Exception:
                    pass
        except Exception:
            pass


# ── Función de conveniencia para el asistente ─────────────────────

def interpretar_comando_musica(query: str, player: PlayerMusica) -> bool:
    """
    Interpreta un comando de voz relacionado con música y
    llama al player correspondiente.

    Args:
        query: Texto reconocido por el STT (en minúsculas).
        player: Instancia de PlayerMusica.

    Returns:
        True si el comando fue de música, False si no aplica.
    """
    q = query.lower()

    # ── Pausar ────────────────────────────────────────────────────
    if any(p in q for p in ['pausa', 'pausar', 'para la música', 'silencia']):
        player.pausar()
        return True

    # ── Reanudar ──────────────────────────────────────────────────
    if any(p in q for p in ['reanuda', 'continúa', 'sigue la música', 'play']):
        player.reanudar()
        return True

    # ── Siguiente ─────────────────────────────────────────────────
    if any(p in q for p in ['siguiente', 'otra canción', 'cambia la canción', 'skip']):
        player.siguiente()
        return True

    # ── Detener ───────────────────────────────────────────────────
    if any(p in q for p in ['detén la música', 'apaga la música', 'deja de tocar',
                             'para ya la música', 'stop música']):
        player.detener()
        return True

    # ── Reproducir ────────────────────────────────────────────────
    triggers_musica = [
        'pon música', 'toca música', 'reproduce música', 'quiero música',
        'escuchar música', 'pon una canción', 'toca una canción',
        'pon salsa', 'toca salsa', 'pon vallenato', 'toca vallenato',
        'pon cumbia', 'pon rock', 'pon pop', 'pon jazz', 'pon balada',
        'música relajante', 'música para trabajar', 'música para estudiar',
        'música tropical', 'música clásica', 'pon reggaeton',
    ]

    for trigger in triggers_musica:
        if trigger in q:
            # Extraer qué canción/género quieren
            busqueda = _extraer_busqueda(q)
            player.reproducir(busqueda)
            return True

    return False


def _extraer_busqueda(query: str) -> str:
    """Extrae el término de búsqueda de un comando de voz."""
    # Remover frases de comando para quedarse solo con el tema
    frases_comando = [
        'pon música de', 'toca música de', 'reproduce', 'pon', 'toca',
        'quiero escuchar', 'quiero música de', 'ponme', 'pon una canción de',
        'música de', 'una canción de', 'canciones de',
    ]
    resultado = query
    for frase in sorted(frases_comando, key=len, reverse=True):
        resultado = resultado.replace(frase, '').strip()

    return resultado if resultado else 'música latina mix'
