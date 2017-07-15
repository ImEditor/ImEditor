#!/usr/bin/python

from os import stat, path
import datetime


def get_middle_mouse(size, mouse_coords):
    width, height = size
    x = mouse_coords[0] - (width / 2)
    y = mouse_coords[1] - (height / 2)
    return (round(x), round(y))


def get_infos(image):
    img_infos = {}
    img = image.get_current_img()
    img_infos['mode'] = img.mode
    img_infos['size'] = '{} x {} pixels'.format(str(img.width), str(img.height))
    if path.isfile(image.filename):
        img_stat = stat(image.filename)
        img_infos['weight'] = '{}ko ({}o)'.format(str(round(img_stat.st_size / 1000, 2)), str(round(img_stat.st_size, 2)))
        img_infos['path'] = image.filename
        img_infos['last_access'] = datetime.datetime.fromtimestamp(img_stat.st_atime).strftime('%d/%m/%Y %Hh%M')
        img_infos['last_change'] = datetime.datetime.fromtimestamp(img_stat.st_mtime).strftime('%d/%m/%Y %Hh%M')
    return img_infos
