#!/usr/bin/python

from os import stat
import datetime


def get_middle_mouse(size, mouse_coords):
    width = size[0]
    height = size[1]
    x = mouse_coords[0] - (width / 2)
    y = mouse_coords[1] - (height / 2)
    return (round(x), round(y))


def get_infos(image):
    img_infos = {}
    img = image.get_current_img()

    img_infos['mode'] = img.mode
    img_infos['size'] = str(img.width) + 'x' + str(img.height)
    if image.filename != 'untitled.png':
        img_stat = stat(image.filename)
        img_infos['weight'] = str(round(img_stat.st_size / 1000, 2)) + ' ko (' + str(round(img_stat.st_size, 2)) + ' o)'
        img_infos['path'] = image.filename
        img_infos['last_access'] = datetime.datetime.fromtimestamp(img_stat.st_atime).strftime('%d/%m/%Y %Hh%M')
        img_infos['last_change'] = datetime.datetime.fromtimestamp(img_stat.st_mtime).strftime('%d/%m/%Y %Hh%M')

    return img_infos
