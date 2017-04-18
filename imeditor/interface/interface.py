#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from PIL import Image
import sys
from os import path

from interface.tab import Tab
from interface.menus import create_menubar, create_toolbar
from interface import dialog
from editor.editor import Editor


class Interface(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title='ImEditor', application=app)
        self.set_size_request(700, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.logo = GdkPixbuf.Pixbuf.new_from_file('assets/icons/icon.png')
        self.set_icon(self.logo)

        grid = Gtk.Grid()

        self.editor = Editor(self)

        # Menubar
        create_menubar(self, app.menu_info)
        # Toolbar
        toolbar = create_toolbar(self)
        # Homepage
        self.homepage = Gtk.Grid(row_spacing=20, column_spacing=20, margin_top=120)
        self.homepage.set_halign(Gtk.Align.CENTER)
        label = Gtk.Label()
        label.set_markup("<span size=\"xx-large\">Que souhaitez-vous faire?</span>")
        new_button = Gtk.Button("Créer une nouvelle image", always_show_image=True)
        new_button.set_image(Gtk.Image.new_from_icon_name('document-new',  Gtk.IconSize.BUTTON))
        new_button.set_action_name('win.new')
        open_button = Gtk.Button("Ouvrir une image existante", always_show_image=True)
        open_button.set_image(Gtk.Image.new_from_icon_name('document-open', Gtk.IconSize.BUTTON))
        open_button.set_action_name('win.open')
        self.homepage.attach(label, 0, 0, 2, 1)
        self.homepage.attach(new_button, 0, 1, 1, 1)
        self.homepage.attach(open_button, 1, 1, 1, 1)
        # Tabs
        self.notebook = Gtk.Notebook()

        grid.attach(toolbar, 0, 0, 1, 1)
        grid.attach(self.notebook, 0, 1, 1, 1)
        grid.attach(self.homepage, 0, 2, 1, 1)
        self.add(grid)

        # Cursors
        display = Gdk.Display.get_default()
        self.default_cursor = Gdk.Cursor.new_from_name(display, "default")
        self.draw_cursor = Gdk.Cursor.new_for_display(display, Gdk.CursorType.PENCIL)
        self.move_cursor = Gdk.Cursor.new_from_name(display, "move")

    def quit(self, action, parameter):
        nb_tabs = self.notebook.get_n_pages()
        for _ in range(nb_tabs):
            self.close_tab(self.notebook.get_current_page())
        sys.exit()

    def new_image(self, action, parameter):
        new_image_dialog = dialog.new_image_dialog(self)
        values = new_image_dialog.get_values()
        img = Image.new('RGB', values[0], values[1])
        self.editor.add_image(img, 'sans-titre.png', 0, False, True)
        self.create_tab(img)

    def open_image(self, action, parameter):
        filename = dialog.file_dialog(self, 'open')
        if filename:
            if path.splitext(filename)[-1] in (".png", ".jpeg", ".jpg"):
                img = Image.open(filename)
                self.editor.add_image(img, filename, 0, True)
                self.create_tab(img, path.basename(filename))
            else:
                error_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, "Une erreur est survenue...")
                error_dialog.format_secondary_text(
                    "Le format de ce fichier n'est pas pris en charge.")
                error_dialog.run()
                error_dialog.destroy()

    def create_tab(self, img, title='Sans titre'):
        tab = Tab(self, img, title)
        page_num = self.notebook.get_current_page() + 1
        self.homepage.hide()
        self.notebook.insert_page(tab, tab.tab_label, page_num)
        self.notebook.show_all()
        self.notebook.set_current_page(page_num)

    def on_close_tab_clicked(self, button, box):
        page_num = self.notebook.page_num(box)
        self.close_tab(page_num)

    def close_tab(self, page_num):
        if not self.editor.images[page_num].saved:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                Gtk.ButtonsType.YES_NO,
                'Enregistrer ' + self.editor.images[page_num].filename + ' avant la fermeture ?')
            dialog.format_secondary_text(
                'Vos modifications seront perdues si vous ne faites pas de sauvegarde.')
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                self.editor.file_save_as(None, None)
                self.notebook.remove_page(page_num)
                self.editor.close_image(page_num)
            elif response == Gtk.ResponseType.NO:
                self.notebook.remove_page(page_num)
                self.editor.close_image(page_num)
            dialog.destroy()
        else:
            self.notebook.remove_page(page_num)
            self.editor.close_image(page_num)

        if self.notebook.get_n_pages() == 0:
            self.homepage.show()

    def update_image(self, new_img):
        page_num = self.notebook.get_current_page()
        tab = self.notebook.get_nth_page(page_num)
        tab.update_image(new_img)
        tab.tab_label.set_icon(new_img)

    def set_fullscreen(self, action, parameter):
        if not self.get_window().get_state() & Gdk.WindowState.FULLSCREEN != 0:
            self.fullscreen_button.set_icon_name('view-restore')
            self.fullscreen()
        else:
            self.fullscreen_button.set_icon_name('view-fullscreen')
            self.unfullscreen()

    def about(self, action, parameter):
        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_logo(self.logo)
        dialog.set_program_name('ImEditor')
        dialog.set_version('0.1')
        dialog.set_website('https://imeditor.github.io')
        dialog.set_authors(['Nathan Seva', 'Hugo Posnic'])
        dialog.set_comments('GTK3 Image Editor')
        dialog.set_license('Distributed under the GNU GPL(v3) license. \n\nhttps://github.com/ImEditor/ImEditor/blob/master/LICENSE')
        dialog.run()
        dialog.destroy()
