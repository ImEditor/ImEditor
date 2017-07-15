#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from PIL import Image, __version__ as pil_version
from os import path

from interface.tab import Tab
from interface.menus import create_menubar, create_toolbar
from interface import dialog


class Interface(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title='ImEditor', application=app)
        self.connect('delete-event', self.quit_app)
        self.app = app
        self.set_size_request(950, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.logo = GdkPixbuf.Pixbuf.new_from_file('assets/icon.png')
        self.set_icon(self.logo)

        # Menubar
        create_menubar(self, app.menu_info)

        # Toolbar
        toolbar = create_toolbar(self)

        # Homepage
        self.homepage = Gtk.Grid(row_spacing=20, column_spacing=20, margin_top=120)
        self.homepage.set_halign(Gtk.Align.CENTER)
        label = Gtk.Label()
        label.set_markup('<span size="xx-large">What do you want to do?</span>')
        new_button = Gtk.Button('Create a new image', always_show_image=True)
        new_button.set_image(Gtk.Image.new_from_icon_name('document-new',  Gtk.IconSize.BUTTON))
        new_button.set_action_name('win.new')
        open_button = Gtk.Button('Open an existing image', always_show_image=True)
        open_button.set_image(Gtk.Image.new_from_icon_name('document-open', Gtk.IconSize.BUTTON))
        open_button.set_action_name('win.open')
        self.homepage.attach(label, 0, 0, 2, 1)
        self.homepage.attach(new_button, 0, 1, 1, 1)
        self.homepage.attach(open_button, 1, 1, 1, 1)

        # Tabs
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.add(toolbar)
        main_box.add(self.notebook)
        main_box.add(self.homepage)
        self.add(main_box)

        # Cursors
        display = Gdk.Display.get_default()
        self.default_cursor = Gdk.Cursor.new_from_name(display, 'default')
        self.draw_cursor = Gdk.Cursor.new_for_display(display, Gdk.CursorType.PENCIL)
        self.move_cursor = Gdk.Cursor.new_from_name(display, 'move')

        # Vars
        self.allowed_formats = ('bmp', 'ico', 'jpeg', 'jpg', 'png', 'webp')
        self.show_all()
        self.notebook.hide()

    def get_tab(self, page_num=None):
        if not page_num:
            page_num = self.notebook.get_current_page()
        tab = self.notebook.get_nth_page(page_num)
        return tab

    def create_tab(self, img, filename, saved=True):
        tab = Tab(self, img, path.basename(filename), filename, saved)
        page_num = self.notebook.get_current_page() + 1
        nb_tabs = self.notebook.get_n_pages()
        self.notebook.insert_page(tab, tab.tab_label, page_num)
        if nb_tabs == 0:
            self.homepage.hide()
            self.notebook.show()
        self.notebook.set_current_page(page_num)

    # Callbacks

    def new_image(self, action, parameter):
        new_image_dialog = dialog.new_image_dialog(self)
        values = new_image_dialog.get_values()
        if values:
            if values[4]:
                mode = 'RGBA'
                color = values[2][:-1] + ',0)'
                color = color.replace('rgb', "rgba")
            else:
                mode = 'RGB'
                color = values[2]
            img = Image.new(mode, values[1], color)
            name = values[0] if values[0] else 'untitled'
            filename = name + '.' + values[3].lower()
            self.create_tab(img, filename, False)

    def open_image(self, action, parameter):
        filename = dialog.file_dialog(self, 'open')
        if filename:
            if path.splitext(filename)[-1][1:].lower() in self.allowed_formats:
                img = Image.open(filename)
                self.create_tab(img, filename)
            else:
                error_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, 'An error has occurred...')
                error_dialog.format_secondary_text(
                    'The format of this file is not supported.')
                error_dialog.run()
                error_dialog.destroy()

    def close_tab(self, action=None, parameter=None, page_num=None):
        if page_num is None:
            page_num = self.notebook.get_current_page()
        tab = self.get_tab(page_num)
        if not tab.editor.image.saved:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                Gtk.ButtonsType.YES_NO,
                'Save ' + path.basename(tab.editor.image.filename) + ' before closing?')
            dialog.format_secondary_text(
                'Your work will be lost if you don\'t make a back up.')
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                tab.save_as()
            tab.editor.close_image()
            self.notebook.remove_page(page_num)
            dialog.destroy()
        else:
            tab.editor.close_image()
            self.notebook.remove_page(page_num)

        if self.notebook.get_n_pages() == 0:
            self.notebook.hide()
            self.homepage.show()

    def save(self, action, parameter):
        tab = self.get_tab()
        tab.editor.save_as()

    def save_as(self, action=None, parameter=None):
        tab = self.get_tab()
        tab.editor.save_as()

    def details(self, action, parameter):
        tab = self.get_tab()
        tab.editor.details()

    def select(self, action=None, parameter=None):
        tab = self.get_tab()
        tab.editor.select()

    def history(self, action, parameter, num):
        tab = self.get_tab()
        tab.editor.history(num)

    def copy(self, action, parameter):
        tab = self.get_tab()
        tab.editor.copy()

    def paste(self, action, parameter):
        tab = self.get_tab()
        tab.editor.paste()

    def cut(self, action, parameter):
        tab = self.get_tab()
        tab.editor.cut()

    def pencil(self, action, parameter):
        tab = self.get_tab()
        tab.editor.pencil()

    def apply_filter(self, action, parameter, func, value=None):
        tab = self.get_tab()
        tab.editor.apply_filter(func, value)

    def apply_filter_with_params(self, action, parameter, params):
        tab = self.get_tab()
        tab.editor.apply_filter_with_params(params)

    def set_fullscreen(self, action, parameter):
        if not self.get_window().get_state() & Gdk.WindowState.FULLSCREEN != 0:
            self.fullscreen_button.set_icon_name('view-restore')
            self.fullscreen()
        else:
            self.fullscreen_button.set_icon_name('view-fullscreen')
            self.unfullscreen()

    def quit_app(self, action=None, parameter=None):
        for i in reversed(range(self.notebook.get_n_pages())):
            self.close_tab(page_num=i)
        self.app.quit()
        return False

    def about(self, action, parameter):
        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_logo(self.logo)
        dialog.set_program_name('ImEditor')
        dialog.set_version('0.1-dev')
        dialog.set_website('https://imeditor.github.io')
        dialog.set_authors(['Nathan Seva', 'Hugo Posnic'])
        dialog.set_comments('Simple & versatile image editor.\n\nPillow: ' + pil_version)
        dialog.set_license('Distributed under the GNU GPL(v3) license. \nhttps://github.com/ImEditor/ImEditor/blob/master/LICENSE\nIcons made by Madebyoliver under CC 3.0 BY.\nhttp://www.flaticon.com/authors/madebyoliver')
        dialog.run()
        dialog.destroy()
