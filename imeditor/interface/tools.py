#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib


def pil_to_pixbuf(img):
    img = img.convert('RGBA')
    data = img.tobytes()
    w, h = img.size
    data = GLib.Bytes.new(data)
    pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, True, 8, w, h, w * 4)
    return pixbuf


class SpinButton(Gtk.SpinButton):
    def __init__(self, default, min_value, max_value, step=20, page=40):
        Gtk.SpinButton.__init__(self)
        self.set_digits(0)
        self.set_numeric(False)
        self.set_range(min_value, max_value)
        self.set_value(default)
        self.set_increments(step, page)
