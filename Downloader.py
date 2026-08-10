#!/usr/bin/env python3
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
"""

import argparse
import sys
import shutil

try:
    import yt_dlp
except ImportError:
    print("❌ Falta la librería yt-dlp. Instálala con:\n    pip install yt-dlp")
    sys.exit(1)


def construir_opciones(args):
    opciones = {
        "outtmpl": f"{args.salida}/%(title)s.%(ext)s",
        "noplaylist": not args.playlist,
        "quiet": False,
        "no_warnings": False,
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

    return opciones


def mostrar_progreso(d):
    if d["status"] == "downloading":
        porcentaje = d.get("_percent_str", "").strip()
        velocidad = d.get("_speed_str", "").strip()
        print(f"\rDescargando... {porcentaje} a {velocidad}", end="", flush=True)
    elif d["status"] == "finished":
        print("\nDescarga completada, procesando archivo...")


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

    args = parser.parse_args()
    opciones = construir_opciones(args)

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([args.url])
        print("\n✅ Descarga finalizada con éxito.")
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error al descargar: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()