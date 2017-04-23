#!/usr/bin/python

from PIL import ImageDraw


def draw_shape(img, shape, coords, fill, color, size):
    if size > 0:
        size /= 2
    x = [coords[0][0] - size, coords[0][1] - size]
    y = [coords[1][0] + size, coords[1][1] + size]

    draw = ImageDraw.Draw(img)
    if shape == 'rectangle':
        if fill:
            draw.rectangle(x + y, fill=color)
        else:
            draw.rectangle(x + y, outline=color)
    elif shape == 'ellipse':
        if fill:
            draw.ellipse(x + y, fill=color)
        else:
            draw.ellipse(x + y, outline=color)
