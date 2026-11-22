#!/usr/bin/env python3
"""Fotos para Mercado Libre / Amazon: fondo blanco puro, sin texto, sin precios, sin sombras.

Genera 1200x1200 en out-marketplace/:
  01-principal-pack.png   (los 4 productos juntos, para la foto principal del pack)
  02..05                  (cada producto solo, para fotos secundarias)

Entrada: src/*_hi.jpg (fotos de catalogo, ilustrativas). Lo ideal es reemplazarlas por
fotos reales de TUS cajas (hoja blanca + luz de ventana) y correr este mismo script.
Uso: python3 make_marketplace.py
"""
import os
from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "src"), os.path.join(HERE, "out-marketplace")
SIZE, FILL = 1200, 1080  # lienzo y area maxima del producto (90% del encuadre)
os.makedirs(OUT, exist_ok=True)
WHITE = (255, 255, 255)


def load(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    w, h = im.size
    for pt in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):  # fondo conectado a las esquinas -> blanco puro
        ImageDraw.floodfill(im, pt, WHITE, thresh=14)
    bbox = ImageChops.difference(im, Image.new("RGB", im.size, WHITE)).convert("L").point(lambda v: 255 if v > 10 else 0).getbbox()
    return im.crop(bbox)


def fit(im, max_w, max_h):
    s = min(max_w / im.width, max_h / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def canvas():
    return Image.new("RGB", (SIZE, SIZE), WHITE)


def paste_center(cv, im, cx, cy):
    cv.paste(im, (round(cx - im.width / 2), round(cy - im.height / 2)))


P = {k: load(f"{k}_hi.jpg") for k in ("bb_etb", "wf_etb", "bb_bundle", "wf_bundle")}

# Individuales
for fn, key in (("02-black-bolt-etb", "bb_etb"), ("03-black-bolt-bundle", "bb_bundle"),
                ("04-white-flare-etb", "wf_etb"), ("05-white-flare-bundle", "wf_bundle")):
    cv = canvas()
    paste_center(cv, fit(P[key], FILL, FILL), SIZE / 2, SIZE / 2)
    cv.save(os.path.join(OUT, fn + ".png"))

# Pack: fila de ETB arriba, fila de bundles abajo (Black Bolt a la izquierda, White Flare a la derecha)
GAP = 30
a_e = P["bb_etb"].width / P["bb_etb"].height
a_b = P["bb_bundle"].width / P["bb_bundle"].height
h1 = min(FILL / (2 * a_e), 470)             # altura de la fila de ETB
h2 = FILL - h1 - GAP                        # altura de la fila de bundles
h2 = min(h2, FILL / (2 * a_b))
total_h = h1 + GAP + h2
top = (SIZE - total_h) / 2
cv = canvas()
for key, col in (("bb_etb", 0), ("wf_etb", 1)):
    im = fit(P[key], FILL / 2 - GAP / 2, h1)
    paste_center(cv, im, SIZE / 2 + (col - 0.5) * (im.width + GAP), top + h1 / 2)
for key, col in (("bb_bundle", 0), ("wf_bundle", 1)):
    im = fit(P[key], FILL / 2 - GAP / 2, h2)
    paste_center(cv, im, SIZE / 2 + (col - 0.5) * (im.width + GAP), top + h1 + GAP + h2 / 2)
cv.save(os.path.join(OUT, "01-principal-pack.png"))

# Verificacion: las 4 esquinas y el borde deben ser blanco puro
for f in sorted(os.listdir(OUT)):
    im = Image.open(os.path.join(OUT, f))
    edge = [im.getpixel((x, y)) for x in (0, SIZE - 1) for y in range(0, SIZE, 50)] + \
           [im.getpixel((x, y)) for y in (0, SIZE - 1) for x in range(0, SIZE, 50)]
    nonwhite = ImageChops.difference(im, Image.new("RGB", im.size, WHITE)).convert("L").point(lambda v: 255 if v > 0 else 0).getbbox()
    print(f, im.size, "borde puro:", all(p == WHITE for p in edge), "producto ocupa:", f"{(nonwhite[2]-nonwhite[0])*100//SIZE}% x {(nonwhite[3]-nonwhite[1])*100//SIZE}%")
