#!/usr/bin/env python3

from PIL import Image

def negative(img):
    """Invert colors of image.
    :param img: image
    :return: PIL object"""
    data = list(img.getdata())
    data_m = list()
    for pixel in data:
        red = 255 - pixel[0]
        green = 255 - pixel[1]
        blue = 255 - pixel[2]
        data_m.append((red, green, blue))
    img_m = Image.new(img.mode, img.size)
    img_m.putdata(data_m)
    return img_m

def red(img):
    data = list(img.getdata())
    data_m = list()
    for pixel in data:
        data_m.append((pixel[0], 0, 0))
    img_m = Image.new(img.mode, img.size)
    img_m.putdata(data_m)
    return img_m

def green(img):
    data = list(img.getdata())
    data_m = list()
    for pixel in data:
        data_m.append((0, pixel[1], 0))
    img_m = Image.new(img.mode, img.size)
    img_m.putdata(data_m)
    return img_m

def blue(img):
    data = list(img.getdata())
    data_m = list()
    for pixel in data:
        data_m.append((0, 0, pixel[2]))
    img_m = Image.new(img.mode, img.size)
    img_m.putdata(data_m)
    return img_m

def grayscale(img):
    data = list(img.getdata())
    data_m = list()
    for pixel in data:
        gray = (pixel[0] + pixel[1] + pixel[2]) // 3
        data_m.append((gray, gray, gray))
    img_m = Image.new(img.mode, img.size)
    img_m.putdata(data_m)
    return img_m

def black_white(img, limit):
    data = list(img.getdata())
    data_m = list()
    for pixel in data:
        gray = (pixel[0] + pixel[1] + pixel[2]) // 3
        gray = 0 if gray < limit else 255
        data_m.append((gray, gray, gray))
    img_m = Image.new(img.mode, img.size)
    img_m.putdata(data_m)
    return img_m

def brightness(img, value):
    data = list(img.getdata())
    data_m = list()
    for pixel in data:
        data_m.append((pixel[0]+value, pixel[1]+value, pixel[2]+value))
    img_m = Image.new(img.mode, img.size)
    img_m.putdata(data_m)
    return img_m

def rotate(img, angle):
    return img.rotate(angle, expand=True)

def horizontal_mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)

def vertical_mirror(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)
