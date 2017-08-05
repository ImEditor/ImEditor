#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib


def pil_to_pixbuf(img):
    data = GLib.Bytes.new(img.tobytes())
    w, h = img.size

    if img.mode != 'RGBA':
        if img.mode != 'RGB':
            img = img.convert('RGB')
        alpha = False
        rowstride = 3
    else:
        alpha = True
        rowstride = 4

    return GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
                alpha, 8, w, h, w * rowstride)


class SpinButton(Gtk.SpinButton):
    def __init__(self, default, min_value, max_value, step=20, page=40):
        Gtk.SpinButton.__init__(self)
        self.set_digits(0)
        self.set_numeric(False)
        self.set_range(min_value, max_value)
        self.set_value(default)
        self.set_increments(step, page)
