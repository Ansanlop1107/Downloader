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
- [`ffmpeg`](https://ffmpeg.org/download.html) (necesario para unir video+audio en MP4 y para extraer MP3)

### Instalación de dependencias

```bash
pip install yt-dlp
```

**ffmpeg:**

| Sistema | Instalación |
|---|---|
| Windows | Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html) y añade la carpeta `bin` al PATH, o instala con `winget install ffmpeg` |
| macOS | `brew install ffmpeg` |
| Linux (Debian/Ubuntu) | `sudo apt install ffmpeg` |

---

## 🚀 Uso

```bash
python descargar_video.py "URL_DEL_VIDEO"
```

### Opciones disponibles

| Opción | Descripción |
|---|---|
| `url` | URL del video o playlist (obligatorio) |
| `-o`, `--salida` | Carpeta donde guardar el archivo (por defecto: carpeta actual) |
| `--solo-audio` | Descarga solo el audio en formato MP3 |
| `--playlist` | Descarga la playlist completa en vez de un solo video |
| `--calidad` | Altura máxima del video en píxeles (ej: `1080`, `720`, `480`) |
| `-h`, `--help` | Muestra la ayuda |

---

## 💡 Ejemplos

**Descargar en la mejor calidad disponible:**
```bash
python descargar_video.py "https://ejemplo.com/video"
```

**Descargar solo el audio en MP3:**
```bash
python descargar_video.py "https://ejemplo.com/video" --solo-audio
```

**Elegir carpeta de salida:**
```bash
python descargar_video.py "https://ejemplo.com/video" -o ~/Descargas
```

**Descargar una playlist completa:**
```bash
python descargar_video.py "https://ejemplo.com/playlist" --playlist
```

**Limitar la calidad máxima a 720p:**
```bash
python descargar_video.py "https://ejemplo.com/video" --calidad 720
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

**`ModuleNotFoundError: No module named 'yt_dlp'`**
Falta instalar la librería: `pip install yt-dlp`

**`error: the following arguments are required: url`**
Olvidaste pasar la URL del video. Debe ir entre comillas como primer argumento:
```bash
python descargar_video.py "https://ejemplo.com/video"
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
