#!/usr/bin/python

from PIL import Image

def negative(img, reverse=False):
    """Invert colors of image.
    :param img: image
    :return: PIL object"""
    data = list(img.getdata())
    for pos, pixel in enumerate(data):
        red = 255 - pixel[0]
        green = 255 - pixel[1]
        blue = 255 - pixel[2]
        data[pos] = (red, green, blue)
    img.putdata(data)
    data = None
    return img

def red(img):
    data = list(img.getdata())
    for pos, pixel in enumerate(data):
        data[pos] = (pixel[0], 0, 0)
    img.putdata(data)
    data = None
    return img

def green(img):
    data = list(img.getdata())
    for pos, pixel in enumerate(data):
        data[pos] = (0, pixel[1], 0)
    img.putdata(data)
    data = None
    return img

def blue(img):
    data = list(img.getdata())
    for pos, pixel in enumerate(data):
        data[pos] = (0, 0, pixel[2])
    img.putdata(data)
    data = None
    return img

def grayscale(img):
    data = list(img.getdata())
    for pos, pixel in enumerate(data):
        gray = (pixel[0] + pixel[1] + pixel[2]) // 3
        data[pos] = (gray, gray, gray)
    img.putdata(data)
    data = None
    return img

def black_white(img, limit):
    data = list(img.getdata())
    for pos, pixel in enumerate(data):
        gray = (pixel[0] + pixel[1] + pixel[2]) // 3
        gray = 0 if gray < limit else 255
        data[pos] = (gray, gray, gray)
    img.putdata(data)
    data = None
    return img

def brightness(img, value, reverse=False):
    print('brightness')
    print(value)
    data = list(img.getdata())
    if reverse:
        value = -value
    # !  if a pixel value is 0, do not add a positive value is reversing
    errors = dict()
    for pos, pixel in enumerate(data):
        red = pixel[0] + value
        green = pixel[1] + value
        blue = pixel[2] + value

        if red > 255 or green > 255 or blue > 255 or red < 0 or green < 0 or blue < 0:
            errors[pos] = (red, green, blue)

        if reverse and errors[pos]:
            red = errors[pos][0]
            green = errors[pos][1]
            blue = errors[pos][2]
            data[pos] = (red + value, green + value, blue + value)
        else:
            data[pos] = (red, green, blue)

    img.putdata(data)
    data = None
    img.save('tests 2em yo.png')
    return img, erros

def rotate(img, angle, reverse=False):
    if not reverse:
        img = img.rotate(angle, expand=True)
    else:
        img = img.rotate(-angle, expand=True)
    return img
