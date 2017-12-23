#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys

from interface.interface import Interface


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        self.win = Interface(self)

    def do_startup(self):
        Gtk.Application.do_startup(self)


if __name__ == '__main__':
    app = Application()
    app.run(sys.argv)
