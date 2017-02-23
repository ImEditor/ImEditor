#!/usr/bin/env python

from PIL import ImageDraw


def draw_point(img, mouse_coords, color='black', size=5):
    draw = ImageDraw.Draw(img)
    x = mouse_coords[0]
    y = mouse_coords[1]
    draw.ellipse([x-size, y-size, x+size, y+size], color)


def draw_shape(img, shape, **kwargs):
    draw = ImageDraw.Draw(img)
    if shape == 'rectangle':
        draw.rectangle(**kwargs)
    elif shape == 'ellipse':
        draw.ellipse(**kwargs)
