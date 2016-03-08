#!/usr/bin/python3

from gi.repository import Gtk
import sys

from interface.interface import App

if __name__ == '__main__':
    app = App()
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        app.open_tab(filename)
        print('open')
    app.show_all()
    Gtk.main()
