#!/usr/bin/env python3

import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio

from .interface import Interface


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                application_id='io.github.ImEditor',
                                flags=Gio.ApplicationFlags.HANDLES_OPEN)

        self.connect('activate', self.show_window)
        self.connect('open', self.open_files)
        self.window = None

    def show_window(self, *args):
        if not self.window:
            self.window = Interface(self)
        else:
            self.window.present()

    def open_files(self, app, files, hint, *args):
        self.show_window()
        for image in files:
            self.window.open_image(filename=image)


def main(version):
    app = Application()
    return app.run(sys.argv)
