"""
Downloader.py - Script para descargar videos con yt-dlp

Requisitos:
    pip install yt-dlp

Uso básico:
    python Downloader.py "https://ejemplo.com/video"

Ejemplos:
    # Descargar en la mejor calidad disponible
    python Downloader.py "URL"

    # Descargar solo audio en mp3
    python Downloader.py "URL" --solo-audio

    # Elegir carpeta de salida
    python Downloader.py "URL" -o ~/Descargas

    # Descargar una playlist completa
    python Downloader.py "URL_PLAYLIST" --playlist

    # Limitar la calidad máxima (ej: 720p)
    python Downloader.py "URL" --calidad 720

    # Forzar un cliente de YouTube (útil si aparece error 403 Forbidden)
    python Downloader.py "URL" --cliente android

    # No limpiar la terminal al iniciar
    python Downloader.py "URL" --sin-limpiar
"""

import argparse
import os
import shutil
import sys
import warnings

# Silenciar warnings de librerías de terceros (requests/urllib3/chardet, etc.)
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

try:
    import yt_dlp
except ImportError:
    print("❌ Falta la librería yt-dlp. Instálala con:\n    pip install yt-dlp")
    sys.exit(1)


class Estilo:
    """Clase para estilos de texto en la terminal usando códigos ANSI."""
    RESET = "\033[0m"
    NEGRITA = "\033[1m"
    CIAN = "\033[36m"
    VERDE = "\033[32m"
    AMARILLO = "\033[33m"
    ROJO = "\033[31m"
    GRIS = "\033[90m"


BANNER = r"""
 ____   _____        ___   _ _     ___    _    ____  _____ ____
|  _ \ / _ \ \      / / \ | | |   / _ \  / \  |  _ \| ____|  _ \
| | | | | | \ \ /\ / /|  \| | |  | | | |/ _ \ | | | |  _| | |_) |
| |_| | |_| |\ V  V / | |\  | |__| |_| / ___ \| |_| | |___|  _ <
|____/ \___/  \_/\_/  |_| \_|_____\___/_/   \_\____/|_____|_| \_\
"""


def limpiar_terminal():
    """Limpia la terminal en Windows, macOS o Linux."""
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_banner():
    ancho = max(68, shutil.get_terminal_size(fallback=(80, 20)).columns - 2)
    ancho = min(ancho, 78)

    subtitulo = "🎬 Descargador de videos"
    firma = "Made with ♥️ by Ansanlop11"

    print(f"{Estilo.CIAN}{Estilo.NEGRITA}\n{BANNER}\n{Estilo.RESET}")
    print(f"{Estilo.GRIS}{'─' * ancho}{Estilo.RESET}")
    print(f"{Estilo.AMARILLO}{Estilo.NEGRITA}{subtitulo.center(ancho)}{Estilo.RESET}")
    print(f"{Estilo.VERDE}{Estilo.NEGRITA}{firma.center(ancho)}{Estilo.RESET}")
    print(f"{Estilo.GRIS}{'─' * ancho}{Estilo.RESET}\n")


def _ancho_barra():
    """Calcula un ancho de barra razonable según el ancho del terminal."""
    columnas = shutil.get_terminal_size(fallback=(80, 20)).columns
    return max(20, min(30, columnas - 55))


def construir_opciones(args):
    opciones = {
        "outtmpl": f"{args.salida}/%(title)s.%(ext)s",
        "noplaylist": not args.playlist,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [mostrar_progreso],
    }

    if args.solo_audio:
        opciones.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        if args.calidad:
            opciones["format"] = (
                f"bestvideo[height<={args.calidad}]+bestaudio/best[height<={args.calidad}]"
            )
        else:
            opciones["format"] = "bestvideo+bestaudio/best"
        opciones["merge_output_format"] = "mp4"

    # Si YouTube empieza a devolver 403, este cliente alternativo suele evitarlo.
    if args.cliente:
        opciones["extractor_args"] = {"youtube": {"player_client": [args.cliente]}}

    return opciones


def mostrar_progreso(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        descargado = d.get("downloaded_bytes", 0)
        porcentaje = (descargado / total * 100) if total else 0.0

        ancho = _ancho_barra()
        llenado = int(ancho * porcentaje / 100)
        barra = "█" * llenado + "░" * (ancho - llenado)

        velocidad = (d.get("_speed_str") or "?").strip()
        eta = (d.get("_eta_str") or "?").strip()

        linea = (
            f"\r⬇️  [{Estilo.CIAN}{barra}{Estilo.RESET}] "
            f"{porcentaje:5.1f}% 🚀 {velocidad:>10} ⏳ ETA {eta:>6}   "
        )
        print(linea, end="", flush=True)

    elif d["status"] == "finished":
        print(f"\n{Estilo.AMARILLO}⚙️  Descarga completa, procesando archivo "
              f"(uniendo/convirtiendo)...{Estilo.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Descarga videos (o audio) de cualquier sitio compatible con yt-dlp."
    )
    parser.add_argument("url", help="URL del video o playlist a descargar")
    parser.add_argument(
        "-o", "--salida", default=".",
        help="Carpeta donde guardar el archivo (por defecto: carpeta actual)"
    )
    parser.add_argument(
        "--solo-audio", action="store_true",
        help="Descargar solo el audio en formato mp3"
    )
    parser.add_argument(
        "--playlist", action="store_true",
        help="Descargar la playlist completa en vez de solo un video"
    )
    parser.add_argument(
        "--calidad", type=int, default=None,
        help="Altura máxima de video en píxeles (ej: 1080, 720, 480)"
    )
    parser.add_argument(
        "--cliente", type=str, default=None, choices=["android", "ios", "web", "tv"],
        help="Forzar un cliente de YouTube específico (útil si aparece error 403)"
    )
    parser.add_argument(
        "--sin-limpiar", action="store_true",
        help="No limpiar la terminal al iniciar"
    )

    args = parser.parse_args()

    if not args.sin_limpiar:
        limpiar_terminal()

    mostrar_banner()

    opciones = construir_opciones(args)

    print(f"{Estilo.NEGRITA}{Estilo.CIAN}🎬 Iniciando descarga de:{Estilo.RESET} {args.url}\n")

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([args.url])
        print(f"\n{Estilo.VERDE}{Estilo.NEGRITA}✅ ¡Descarga finalizada con éxito! 🎉{Estilo.RESET}\n")
    except yt_dlp.utils.DownloadError as e:
        print(f"\n{Estilo.ROJO}❌ Error al descargar:{Estilo.RESET} {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Estilo.AMARILLO}⚠️  Descarga cancelada por el usuario.{Estilo.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()