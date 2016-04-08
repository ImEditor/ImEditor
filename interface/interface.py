#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from PIL import Image
from os import path
import sys

from interface.tabs import Tab
from interface.menus import create_menubar, create_toolbar
from interface import dialog
from editor.editor import Editor

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title='ImEditor', application=app)
        self.set_default_size(700, 500)
        self.set_position(Gtk.WindowPosition.CENTER)

        grid = Gtk.Grid()
        self.add(grid)

        self.editor = Editor()
        self.editor.set_win(self)

        # Menubar:
        create_menubar(self, app.menu_info)
        # Toolbar:
        toolbar = create_toolbar(self)
        grid.attach(toolbar, 0, 0, 1, 1)
        # Tabs:
        self.notebook = Gtk.Notebook()
        grid.attach(self.notebook, 0, 1, 1, 1)

    def quit(self, action, parameter):
        sys.exit()

    def new_image(self, action, parameter):
        new_image_dialog = dialog.new_image_dialog(self)
        values = new_image_dialog.get_values()
        if values is not None:
            img = Image.new('RGB', values[0], values[1])
            self.editor.add_image(img, 'noname.jpg', 0)
            self.create_tab(img)

    def open_image(self, action, parameter):
        filename = dialog.file_dialog(self)
        if filename is not None:
            img = Image.open(filename)
            pos = filename.rfind('/')
            basename = filename[pos+1:]
            self.editor.add_image(img, filename, 0)
            self.create_tab(img, basename)

    def create_tab(self, img, title='Sans-titre'):
        tab = Tab(self, img, title)
        page_num = self.notebook.get_current_page() + 1
        self.notebook.insert_page(tab, tab.get_tab_label(), page_num)
        self.notebook.show_all()
        self.notebook.set_current_page(page_num)

    def on_close_tab_clicked(self, button, box):
        page_num = self.notebook.page_num(box)
        self.close_tab(page_num)

    def close_tab(self, page_num):
        self.notebook.remove_page(page_num)
        self.editor.close_image(page_num)

    def update_image(self, new_img, page):
        tab = self.notebook.get_nth_page(page)
        tab.update_image(new_img)
        tab.tab_label.set_icon(new_img)
        self.notebook.show_all()

    def set_fullscreen(self, action, parameter):
        # check if the state is the same as Gdk.WindowState.FULLSCREEN, which is a bit flag
        is_fullscreen = self.get_window().get_state() & Gdk.WindowState.FULLSCREEN != 0
        if not is_fullscreen:
            self.fullscreen_button.set_icon_name('view-restore')
            self.fullscreen()
        else:
            self.fullscreen_button.set_icon_name('view-fullscreen')
            self.unfullscreen()

    def about(self, action, parameter):
        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file('assets/icons/imeditor.png'))
        dialog.set_program_name('ImEditor')
        dialog.set_version('0.1')
        dialog.set_website('https://github.com/ImEditor')
        dialog.set_authors(['Nathan Seva', 'Hugo Posnic'])
        dialog.set_comments('GTK Linux Image Editor ')
        dialog.set_license('Distributed under the GNU GPL(v3) license. \n\n https://github.com/ImEditor/ImEditor/blob/master/LICENSE')
        dialog.run()
        dialog.destroy()
