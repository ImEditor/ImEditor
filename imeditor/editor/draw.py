#!/usr/bin/python

from PIL import ImageDraw

def draw_shape(img, coords, size):
    draw = ImageDraw.Draw(img)
    if size > 0:
        size /= 2
    x = [coords[0][0] - size, coords[0][1] - size]
    y = [coords[1][0] + size, coords[1][1] + size]
    return draw, size, x + y

def draw_rectangle(img, coords, color, size, fill=True):
    draw, size, xy = draw_shape(img, coords, size)
    if fill:
        draw.rectangle(xy, fill=color)
    else:
        draw.rectangle(xy, outline=color)

def draw_ellipse(img, coords, color, size, fill=True):
    draw, size, xy = draw_shape(img, coords, size)
    if fill:
        draw.ellipse(xy, fill=color)
    else:
        draw.ellipse(xy, outline=color)
