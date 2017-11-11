#!/usr/bin/python

from PIL import ImageDraw

def draw_shape(img, coords, size):
    draw = ImageDraw.Draw(img)
    if size > 0:
        size /= 2
    x = [coords[0][0] - size, coords[0][1] - size]
    y = [coords[1][0] + size, coords[1][1] + size]
    return draw, size, x + y

def draw_rectangle(img, coords, size, fill_color=None, outline_color=None):
    draw, size, xy = draw_shape(img, coords, size)
    draw.rectangle(xy, fill=fill_color, outline=outline_color)

def draw_ellipse(img, coords, size, fill_color=None, outline_color=None):
    draw, size, xy = draw_shape(img, coords, size)
    draw.ellipse(xy, fill=fill_color, outline=outline_color)
