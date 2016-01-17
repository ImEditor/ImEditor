#!/usr/bin/python3

from gi.repository import Gtk

from interface.interface import App

if __name__ == '__main__':
    app = App()
    app.show_all()
    Gtk.main()
