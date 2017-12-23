#!/usr/bin/env python

from os import stat, path
from datetime import datetime


def get_middle_mouse(size, mouse_coords):
    x = mouse_coords[0] - (size[0] / 2)
    y = mouse_coords[1] - (size[1] / 2)
    return (round(x), round(y))

def get_infos(img, filename):
    """Fetch informations about an image"""
    # Basic infos
    img_infos = {
        'name': path.basename(filename),
        'mode': img.mode,
        'size': '{} x {} pixels'.format(str(img.width), str(img.height))
    }
    # Infos available only if the image is saved on the disk
    if path.isfile(filename):
        img_stat = stat(filename)
        img_infos['weight'] = '{}ko ({}o)'.format(str(round(img_stat.st_size / 1000, 2)),
                                                    str(round(img_stat.st_size, 2)))
        img_infos['folder'] = path.dirname(filename)
        img_infos['last_change'] = datetime.fromtimestamp(img_stat.st_mtime).strftime('%d/%m/%Y %Hh%M')
    return img_infos
