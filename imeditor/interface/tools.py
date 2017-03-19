#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib


def pil_to_pixbuf(img):
    data = GLib.Bytes.new(img.tobytes())
    if img.mode == "RGBA":
        pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
                    True, 8, img.width, img.height, img.width * 4)
    else:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
                    False, 8, img.width, img.height, img.width * 3)
    return pixbuf


class SpinButton(Gtk.SpinButton):
    def __init__(self, default, min_value, max_value):
        Gtk.SpinButton.__init__(self)
        self.set_digits(0)
        self.set_numeric(False)
        self.set_range(min_value, max_value)
        self.set_value(default)
        self.set_increments(40, 20)
