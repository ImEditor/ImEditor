#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import sys

from imeditor.interface.interface import Interface


def main():
    app = App()
    app.run(sys.argv)


class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                application_id='io.github.imeditor',
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


if __name__ == '__main__':
    main()
