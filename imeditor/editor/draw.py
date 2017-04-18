#!/usr/bin/python

from PIL import ImageDraw

def draw_point(img, coords, color='black', size=5):
    draw = ImageDraw.Draw(img)
    top_left = (coords[0] - size, coords[1] - size)
    bottom_right = (coords[0] + size, coords[1] + size)
    point = [top_left, bottom_right]
    draw.ellipse(point, color)

def draw_shape(img, shape, **kwargs):
    draw = ImageDraw.Draw(img)
    if shape == 'rectangle':
        draw.rectangle(**kwargs)
    elif shape == 'ellipse':
        draw.ellipse(**kwargs)
