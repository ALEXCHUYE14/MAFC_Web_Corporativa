#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
 MAFC — Soluciones Digitales & Software a Medida
 zip_builder.py · Empaquetador automático del sitio web corporativo
-----------------------------------------------------------------------------
 Recorre la carpeta del proyecto (index.html, /css, /js, /assets, README.md)
 y genera el archivo distribuible:  MAFC_Web_Corporativa.zip

 Uso:
     python3 zip_builder.py
=============================================================================
"""

import os
import sys
import zipfile
from datetime import datetime

# --- Configuración -----------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_NAME = "MAFC_Web_Corporativa.zip"
OUTPUT_PATH = os.path.join(ROOT, OUTPUT_NAME)

# Elementos que SÍ se incluyen en el paquete final (solución completa)
INCLUDE = [
    "index.html",
    "README.md",
    "robots.txt",
    "sitemap.xml",
    "css",
    "js",
    "assets",
    "public",              # logo real + capturas reales del portafolio
    "gen_assets.py",      # generador de los mockups SVG
    "zip_builder.py",     # este mismo empaquetador
]

# Archivos/carpetas que NUNCA se incluyen
EXCLUDE_NAMES = {
    OUTPUT_NAME,          # el propio zip
    "shot_test.py",       # script de pruebas de render
    "__pycache__",
    ".DS_Store",
    "Thumbs.db",
    ".git",
    ".gitignore",
}


def human_size(num_bytes):
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"


def iter_files():
    """Genera (ruta_absoluta, ruta_relativa) de todos los archivos a empaquetar."""
    for item in INCLUDE:
        abs_item = os.path.join(ROOT, item)
        if not os.path.exists(abs_item):
            print(f"  ⚠  Aviso: '{item}' no existe, se omite.")
            continue

        if os.path.isfile(abs_item):
            yield abs_item, os.path.relpath(abs_item, ROOT)
            continue

        # Es un directorio: recorrer recursivamente
        for dirpath, dirnames, filenames in os.walk(abs_item):
            # Filtrar directorios excluidos in-place
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_NAMES]
            for fname in filenames:
                if fname in EXCLUDE_NAMES:
                    continue
                abs_file = os.path.join(dirpath, fname)
                rel_file = os.path.relpath(abs_file, ROOT)
                yield abs_file, rel_file


def build_zip():
    print("=" * 62)
    print(" MAFC · Empaquetando sitio web corporativo")
    print("=" * 62)

    # Eliminar zip previo para evitar residuos
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
        print(f"  ↺  Reemplazando paquete anterior…")

    files = list(iter_files())
    if not files:
        print("  ✖  No se encontraron archivos para empaquetar. Abortando.")
        sys.exit(1)

    total_bytes = 0
    with zipfile.ZipFile(OUTPUT_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for abs_file, rel_file in sorted(files, key=lambda t: t[1]):
            # Normalizar separadores a "/" para compatibilidad multiplataforma
            arcname = rel_file.replace(os.sep, "/")
            zf.write(abs_file, arcname)
            size = os.path.getsize(abs_file)
            total_bytes += size
            print(f"  +  {arcname:<42} {human_size(size):>10}")

    zip_size = os.path.getsize(OUTPUT_PATH)
    print("-" * 62)
    print(f"  ✔  Archivos empaquetados : {len(files)}")
    print(f"  ✔  Tamaño sin comprimir  : {human_size(total_bytes)}")
    print(f"  ✔  Tamaño del ZIP        : {human_size(zip_size)}")
    print(f"  ✔  Generado              : {OUTPUT_NAME}")
    print(f"  ✔  Fecha                 : {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 62)
    print(" Listo. Descomprime el ZIP y abre 'index.html' en tu navegador.")
    print("=" * 62)


if __name__ == "__main__":
    build_zip()
