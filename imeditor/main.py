# -*- coding: utf-8 -*-
#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
import json
from collections import OrderedDict

from interface.interface import Window

class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.ui_info, self.menu_info = self.get_ui()

    def do_activate(self):
        self.win = Window(self)
        self.win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder()
        builder.add_from_string(self.ui_info)

        self.set_menubar(builder.get_object('menubar'))

    def get_ui(self):
        ui = '<interface><menu id="menubar">'
        with open('interface/menus.json', 'r') as myfile:
            menu = json.load(myfile, object_pairs_hook=OrderedDict)

        for submenu in menu:
            ui += '<submenu><attribute name="label">' + submenu + '</attribute><section>'
            for act in menu[submenu]:
                ui += '<item>'
                ui += '<attribute name="label">' + act['label'] + '</attribute>'
                ui += '<attribute name="action">win.' + act['name'] + '</attribute>'
                if 'shortcut' in act.keys():
                    ui += '<attribute name="accel">' + act['shortcut'] + '</attribute>'
                ui += '</item>'
            ui += '</section></submenu>'
        ui += '</menu></interface>'
        return ui, menu

if __name__ == '__main__':
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
