#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib
from io import BytesIO

def pil_to_pixbuf(img):
    data = img.tobytes()
    w, h = img.size
    data = GLib.Bytes.new(data)
    pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, w, h, w * 3)

    return pixbuf

class SpinButton(Gtk.SpinButton):
    def __init__(self, default, min_value, max_value):
        Gtk.SpinButton.__init__(self)
        self.set_digits(0)
        self.set_numeric(False)
        self.set_range(min_value, max_value)
        self.set_value(default)
        self.set_increments(40, 20)
