#!/usr/bin/env python

from collections import OrderedDict
from os import stat
import datetime
from platform import system


def get_middle_mouse(size, mouse_coords):
    width = size[0]
    height = size[1]
    x = mouse_coords[0] - (width / 2)
    y = mouse_coords[1] - (height / 2)
    return round(x), round(y)


def get_infos(image):
    img_infos = OrderedDict()
    filename = image.filename
    img = image.get_current_img()

    img_infos['mode'] = img.mode
    img_infos['dimensions'] = str(img.width) + 'x' + str(img.height)
    if filename != 'sans-titre.png':
        img_stat = stat(filename)
        img_infos['taille'] = str(round(img_stat.st_size / 1000, 2)) + ' ko (' + str(round(img_stat.st_size, 2)) + ' o)'
        img_infos['chemin'] = filename
        if system() == 'Windows':
            img_infos['création'] = datetime.datetime.fromtimestamp(img_stat.st_birthtime).strftime('%d/%m/%Y %Hh%M')
        img_infos['dernier accès'] = datetime.datetime.fromtimestamp(img_stat.st_atime).strftime('%d/%m/%Y %Hh%M')
        img_infos['dernière modification'] = datetime.datetime.fromtimestamp(img_stat.st_mtime).strftime('%d/%m/%Y %Hh%M')

    return img_infos
