#!/usr/bin/env python3

from PIL import ImageDraw


def draw_shape(img, coords, size):
    """Prepare the draw object"""
    draw = ImageDraw.Draw(img)
    if size > 0:
        size /= 2
    x = [coords[0][0] - size, coords[0][1] - size]
    y = [coords[1][0] + size, coords[1][1] + size]
    return draw, x + y

def draw_rectangle(img, coords, size, fill_color=None, outline_color=None):
    """Draw a rectangle on an image"""
    draw, xy = draw_shape(img, coords, size)
    draw.rectangle(xy, fill=fill_color, outline=outline_color)
    return xy

def draw_ellipse(img, coords, size, fill_color=None, outline_color=None):
    """Draw an ellipse on an image"""
    draw, xy = draw_shape(img, coords, size)
    draw.ellipse(xy, fill=fill_color, outline=outline_color)
    return xy

def draw_line(img, coords, size, fill_color=None):
    """Draw a line on an image"""
    draw, xy = draw_shape(img, coords, size)
    draw.line(xy, fill=fill_color, width=size)
