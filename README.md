# 🎬 Descargar Video

Script de línea de comandos en Python para descargar videos (o solo audio) desde cualquier plataforma compatible con [`yt-dlp`](https://github.com/yt-dlp/yt-dlp): YouTube, Vimeo, Twitter/X, TikTok, Dailymotion, y muchas más.

Incluye barra de progreso visual en tiempo real, selección de calidad, extracción de audio a MP3 y soporte para playlists.

---

## ✨ Características

- ⬇️ Descarga de video en la mejor calidad disponible (o limitada a una resolución específica)
- 🎵 Extracción de solo audio en formato MP3
- 📃 Descarga de playlists completas
- 📊 Barra de progreso visual con velocidad y tiempo estimado (ETA)
- 📁 Carpeta de salida configurable
- ✅ Manejo de errores claro, con mensajes en español

---

## 📦 Requisitos

- Python 3.8 o superior
- [`yt-dlp`](https://pypi.org/project/yt-dlp/)
- [`ffmpeg`](https://ffmpeg.org/download.html) (**necesario** para unir video+audio en MP4 y para extraer MP3 — sin él, la descarga falla en cuanto yt-dlp necesita combinar streams separados)

### 🔧 Instalación de dependencias

**1. Clona o descarga el proyecto**, y sitúate en su carpeta:

```bash
cd Downloader
```

**2. Instala las dependencias de Python.**

Con el archivo `requirements.txt` incluido en el proyecto:

```bash
pip install -r requirements.txt
```

O manualmente, instalando solo `yt-dlp`:

```bash
pip install yt-dlp
```

> 💡 Se recomienda usar un entorno virtual para no mezclar dependencias con otros proyectos:
> ```bash
> python -m venv venv
> venv\Scripts\activate      # Windows
> source venv/bin/activate   # macOS / Linux
> pip install -r requirements.txt
> ```

**3. Instala ffmpeg** (obligatorio, ver tabla abajo).

**4. Verifica que todo está listo:**

```bash
python -c "import yt_dlp; print('yt-dlp OK')"
ffmpeg -version
```

Si ambos comandos responden sin error, ya puedes usar el script.

**ffmpeg:**

| Sistema | Instalación |
|---|---|
| Windows | `winget install ffmpeg` (recomendado), o descarga desde [ffmpeg.org](https://ffmpeg.org/download.html) y añade la carpeta `bin` al PATH |
| macOS | `brew install ffmpeg` |
| Linux (Debian/Ubuntu) | `sudo apt install ffmpeg` |

> ⚠️ Tras instalar con `winget`, cierra y vuelve a abrir la terminal para que reconozca el PATH actualizado.

### (Opcional) Runtime de JavaScript para YouTube

yt-dlp puede mostrar esta advertencia al descargar de YouTube:

```
WARNING: [youtube] No supported JavaScript runtime could be found...
```

No detiene la descarga, pero sin un runtime de JS (como [`deno`](https://deno.com/)) yt-dlp puede no obtener todos los formatos disponibles. Es opcional instalarlo; si quieres eliminar la advertencia y tener acceso a todos los formatos, instala `deno` y sigue las instrucciones del [wiki de yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/EJS).

---

## 🚀 Uso

```bash
python Downloader.py "URL_DEL_VIDEO"
```

### Opciones disponibles

| Opción | Descripción |
|---|---|
| `url` | URL del video o playlist (obligatorio) |
| `-o`, `--salida` | Carpeta donde guardar el archivo (por defecto: carpeta actual) |
| `--solo-audio` | Descarga solo el audio en formato MP3 |
| `--playlist` | Descarga la playlist completa en vez de un solo video |
| `--calidad` | Altura máxima del video en píxeles (ej: `1080`, `720`, `480`) |
| `--cliente` | Cliente de YouTube específico: `android`, `ios`, `web`, `tv` |
| `-c`, `--cookies` | Archivo `cookies.txt` para autenticación (videos privados, TikTok, YouTube +18) |
| `-cb`, `--cookies-from-browser` | Extraer cookies del navegador (`firefox`, `edge`, `chrome`, etc.) |
| `--sin-limpiar` | No limpiar la terminal al iniciar |
| `-h`, `--help` | Muestra la ayuda |

---

## 💡 Ejemplos

**Descargar en la mejor calidad disponible:**
```bash
python Downloader.py "https://ejemplo.com/video"
```

**Descargar solo el audio en MP3:**
```bash
python Downloader.py "https://ejemplo.com/video" --solo-audio
```

**Elegir carpeta de salida:**
```bash
python Downloader.py "https://ejemplo.com/video" -o ~/Descargas
```

**Descargar una playlist completa:**
```bash
python Downloader.py "https://ejemplo.com/playlist" --playlist
```

**Limitar la calidad máxima a 720p:**
```bash
python Downloader.py "https://ejemplo.com/video" --calidad 720
```

**Descargar videos privados o que requieren login (TikTok, YouTube +18, etc.):**
```bash
# Método recomendado (100% fiable): usando archivo cookies.txt
python Downloader.py "https://www.tiktok.com/@usuario/video/..." --cookies cookies.txt

# O extrayendo cookies de un navegador compatible (ej: firefox):
python Downloader.py "https://www.tiktok.com/@usuario/video/..." --cookies-from-browser firefox
```

---

## 🖥️ Ejemplo de salida

```
🎬 Iniciando descarga de: https://ejemplo.com/video

⬇️  [███████████████░░░░░░░░░░░░░░]  52.3% 🚀 4.2MiB/s ⏳ ETA 00:12
⚙️  Descarga completa, procesando archivo (uniendo/convirtiendo)...

✅ ¡Descarga finalizada con éxito! 🎉
```

---

## 🛠️ Solución de problemas

**`ERROR: [TikTok] ... You do not have permission to view this post`**
Este error ocurre cuando el video de TikTok es privado, de una cuenta privada, para amigos, o cuando TikTok bloquea peticiones anónimas requiriendo autenticación:
1. Instala una extensión para exportar cookies en formato Netscape, por ejemplo:
   - [Get cookies.txt LOCALLY (Chrome/Edge/Brave)](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - [Cookie-Editor](https://cookie-editor.com/)
2. Abre TikTok en tu navegador e inicia sesión con una cuenta que tenga acceso al video.
3. Abre la extensión, exporta las cookies y guarda el archivo como `cookies.txt` en la misma carpeta del script.
4. Ejecuta:
   ```bash
   python Downloader.py "URL_DEL_TIKTOK" --cookies cookies.txt
   ```

**`ERROR: Failed to decrypt with DPAPI (issue #10927)`**
En Windows, las versiones recientes de Google Chrome y Microsoft Edge protegen sus cookies con una clave de sistema (*App-Bound Encryption*) que impide a programas externos leerlas directamente. Para solucionarlo, usa la opción `--cookies cookies.txt` explicada arriba (o usa Firefox con `--cookies-from-browser firefox`).

**`ModuleNotFoundError: No module named 'yt_dlp'`**
Falta instalar la librería: `pip install yt-dlp`

**`ERROR: You have requested merging of multiple formats but ffmpeg is not installed`**
Necesitas `ffmpeg` instalado y en el PATH para que yt-dlp pueda unir el video y el audio. Instálalo con `winget install ffmpeg` (Windows), `brew install ffmpeg` (macOS) o `sudo apt install ffmpeg` (Linux), y reinicia la terminal.

**`WARNING: [youtube] No supported JavaScript runtime could be found`**
Es solo una advertencia, no detiene la descarga. yt-dlp avisa que sin un runtime de JS (ej. `deno`) podría no obtener todos los formatos disponibles de YouTube. Instalar `deno` es opcional.

**`error: the following arguments are required: url`**
Olvidaste pasar la URL del video. Debe ir entre comillas como argumento:
```bash
python Downloader.py "https://ejemplo.com/video"
```

**`RequestsDependencyWarning`**
Es solo una advertencia de versiones de dependencias, no detiene la descarga. Si quieres eliminarla:
```bash
pip install --upgrade requests urllib3 charset_normalizer
```

**Error al unir video y audio / no genera MP3**
Asegúrate de tener `ffmpeg` instalado y disponible en el PATH del sistema.

---

## ⚖️ Aviso legal

Este script es una herramienta de uso personal. Respeta siempre los términos de servicio de la plataforma de origen y los derechos de autor del contenido que descargues.