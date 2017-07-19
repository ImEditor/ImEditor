#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
from PIL import Image, __version__ as pil_version
from os import path

from interface.tab import Tab
from interface import dialog


class Interface(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title='ImEditor', application=app)
        self.connect('delete-event', self.quit_app)
        self.app = app
        self.set_default_size(950, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.logo = GdkPixbuf.Pixbuf.new_from_file('assets/icon.png')
        self.set_icon(self.logo)

        # Header Bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = 'ImEditor'
        hb.props.subtitle = 'Simple & versatile image editor'
        self.set_titlebar(hb)

        # Menu
        menu_button = Gtk.MenuButton()
        menu_model = Gio.Menu()
        menu_model.append('Copy', 'win.copy')
        menu_model.append('Paste', 'win.paste')
        menu_model.append('Cut', 'win.cut')
        sub_menu = Gio.Menu()
        sub_menu.append('Black & white', 'win.black-and-white')
        sub_menu.append('Negative', 'win.negative')
        sub_menu.append('Red', 'win.red')
        sub_menu.append('Green', 'win.green')
        sub_menu.append('Blue', 'win.blue')
        sub_menu.append('Grayscale', 'win.grayscale')
        sub_menu.append('Ligthen', 'win.lighten')
        sub_menu.append('Darken', 'win.darken')
        menu_model.append_submenu('Filters', sub_menu)
        menu_model.append('Image details', 'win.details')
        menu_model.append('About', 'win.about')
        menu_button.set_menu_model(menu_model)
        hb.pack_end(menu_button)

        # Actions
        # Pencil
        self.pencil_action = Gio.SimpleAction.new('pencil', None)
        self.pencil_action.connect('activate', self.pencil)
        self.add_action(self.pencil_action)
        self.pencil_button = Gtk.Button()
        self.pencil_button.set_image(Gtk.Image.new_from_file('assets/pencil.png'))
        self.pencil_button.set_action_name('win.pencil')
        hb.pack_end(self.pencil_button)

        # Select
        self.select_action = Gio.SimpleAction.new('select', None)
        self.select_action.connect('activate', self.select)
        self.add_action(self.select_action)
        self.select_button = Gtk.Button()
        self.select_button.set_image(Gtk.Image.new_from_file('assets/select.png'))
        self.select_button.set_action_name('win.select')
        hb.pack_end(self.select_button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), 'linked')

        # New
        self.new_action = Gio.SimpleAction.new('new', None)
        self.new_action.connect('activate', self.new_image)
        self.add_action(self.new_action)
        app.add_accelerator('<Primary>n', 'win.new', None)
        self.new_button = Gtk.Button.new_from_icon_name('document-new', Gtk.IconSize.SMALL_TOOLBAR)
        self.new_button.set_action_name('win.new')
        box.add(self.new_button)

        # Open
        self.open_action = Gio.SimpleAction.new('open', None)
        self.open_action.connect('activate', self.open_image)
        self.add_action(self.open_action)
        app.add_accelerator('<Primary>o', 'win.open', None)
        self.open_button = Gtk.Button.new_from_icon_name('document-open', Gtk.IconSize.SMALL_TOOLBAR)
        self.open_button.set_action_name('win.open')
        box.add(self.open_button)

        # Save
        self.save_action = Gio.SimpleAction.new('save', None)
        self.save_action.connect('activate', self.save)
        self.add_action(self.save_action)
        app.add_accelerator('<Primary>s', 'win.save', None)
        self.save_button = Gtk.Button.new_from_icon_name('document-save', Gtk.IconSize.SMALL_TOOLBAR)
        self.save_button.set_action_name('win.save')
        box.add(self.save_button)

        # Save as
        self.save_as_action = Gio.SimpleAction.new('save-as', None)
        self.save_as_action.connect('activate', self.save_as)
        self.add_action(self.save_as_action)
        self.save_as_button = Gtk.Button.new_from_icon_name('document-save-as', Gtk.IconSize.SMALL_TOOLBAR)
        self.save_as_button.set_action_name('win.save-as')
        box.add(self.save_as_button)

        # Undo
        self.undo_action = Gio.SimpleAction.new('undo', None)
        self.undo_action.connect('activate', self.history, -1)
        self.add_action(self.undo_action)
        app.add_accelerator('<Primary>z', 'win.undo', None)
        self.undo_button = Gtk.Button.new_from_icon_name('edit-undo', Gtk.IconSize.SMALL_TOOLBAR)
        self.undo_button.set_action_name('win.undo')
        box.add(self.undo_button)

        # Redo
        self.redo_action = Gio.SimpleAction.new('redo', None)
        self.redo_action.connect('activate', self.history, 1)
        self.add_action(self.redo_action)
        app.add_accelerator('<Primary>y', 'win.redo', None)
        self.redo_button = Gtk.Button.new_from_icon_name('edit-redo', Gtk.IconSize.SMALL_TOOLBAR)
        self.redo_button.set_action_name('win.redo')
        box.add(self.redo_button)

        # Rotate left
        self.rotate_left_action = Gio.SimpleAction.new('rotate-left', None)
        self.rotate_left_action.connect('activate', self.apply_filter, 'rotate_left')
        self.add_action(self.rotate_left_action)
        self.rotate_left_button = Gtk.Button.new_from_icon_name('object-rotate-left', Gtk.IconSize.SMALL_TOOLBAR)
        self.rotate_left_button.set_action_name('win.rotate-left')
        box.add(self.rotate_left_button)

        # Rotate right
        self.rotate_right_action = Gio.SimpleAction.new('rotate-right', None)
        self.rotate_right_action.connect('activate', self.apply_filter, 'rotate_right')
        self.add_action(self.rotate_right_action)
        self.rotate_right_button = Gtk.Button.new_from_icon_name('object-rotate-right', Gtk.IconSize.SMALL_TOOLBAR)
        self.rotate_right_button.set_action_name('win.rotate-right')
        box.add(self.rotate_right_button)

        # Copy
        self.copy_action = Gio.SimpleAction.new('copy', None)
        self.copy_action.connect('activate', self.copy)
        self.add_action(self.copy_action)
        app.add_accelerator('<Primary>c', 'win.copy', None)

        # Paste
        self.paste_action = Gio.SimpleAction.new('paste', None)
        self.paste_action.connect('activate', self.paste)
        self.add_action(self.paste_action)
        app.add_accelerator('<Primary>v', 'win.paste', None)

        # Cut
        self.cut_action = Gio.SimpleAction.new('cut', None)
        self.cut_action.connect('activate', self.cut)
        self.add_action(self.cut_action)
        app.add_accelerator('<Primary>x', 'win.cut', None)

        # Details
        self.details_action = Gio.SimpleAction.new('details', None)
        self.details_action.connect('activate', self.details)
        self.add_action(self.details_action)

        # About
        self.about_action = Gio.SimpleAction.new('about', None)
        self.about_action.connect('activate', self.about)
        self.add_action(self.about_action)

        # Filters
        self.black_and_white = Gio.SimpleAction.new('black-and-white', None)
        self.black_and_white.connect('activate', self.apply_filter, 'black_white', ('Black & white', [0, 255]))
        self.add_action(self.black_and_white)

        self.negative = Gio.SimpleAction.new('negative', None)
        self.negative.connect('activate', self.apply_filter, 'negative')
        self.add_action(self.negative)

        self.red = Gio.SimpleAction.new('red', None)
        self.red.connect('activate', self.apply_filter, 'red')
        self.add_action(self.red)

        self.green = Gio.SimpleAction.new('green', None)
        self.green.connect('activate', self.apply_filter, 'green')
        self.add_action(self.green)

        self.blue = Gio.SimpleAction.new('blue', None)
        self.blue.connect('activate', self.apply_filter, 'blue')
        self.add_action(self.blue)

        self.grayscale = Gio.SimpleAction.new('grayscale', None)
        self.grayscale.connect('activate', self.apply_filter, 'grayscale')
        self.add_action(self.grayscale)

        self.lighten = Gio.SimpleAction.new('lighten', None)
        self.lighten.connect('activate', self.apply_filter, 'lighten', ('Lighten', [0, 255]))
        self.add_action(self.lighten)

        self.darken = Gio.SimpleAction.new('darken', None)
        self.darken.connect('activate', self.apply_filter, 'darken', ('Darken', [0, 255]))
        self.add_action(self.darken)

        hb.pack_start(box)
        self.sensitive_toolbar(False)

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
        self.notebook.connect('switch-page', self.on_tab_switched)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
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

    def sensitive_toolbar(self, state):
        self.pencil_action.set_enabled(state)
        self.select_action.set_enabled(state)
        self.save_action.set_enabled(state)
        self.save_as_action.set_enabled(state)
        self.pencil_action.set_enabled(state)
        self.undo_action.set_enabled(state)
        self.redo_action.set_enabled(state)
        self.rotate_left_action.set_enabled(state)
        self.rotate_right_action.set_enabled(state)
        self.copy_action.set_enabled(state)
        self.paste_action.set_enabled(state)
        self.cut_action.set_enabled(state)
        self.details_action.set_enabled(state)
        self.black_and_white.set_enabled(state)
        self.negative.set_enabled(state)
        self.red.set_enabled(state)
        self.green.set_enabled(state)
        self.blue.set_enabled(state)
        self.grayscale.set_enabled(state)
        self.lighten.set_enabled(state)
        self.darken.set_enabled(state)

    def get_tab(self, page_num=None):
        if not page_num:
            page_num = self.notebook.get_current_page()
        return self.notebook.get_nth_page(page_num)

    def create_tab(self, img, filename, saved=True):
        tab = Tab(self, img, path.basename(filename), filename, saved)
        page_num = self.notebook.get_current_page() + 1
        nb_tabs = self.notebook.get_n_pages()
        self.notebook.insert_page(tab, tab.tab_label, page_num)
        if nb_tabs == 0:
            self.homepage.hide()
            self.notebook.show()
        self.notebook.set_current_page(page_num)
        self.sensitive_toolbar(True)

    def on_tab_switched(self, notebook, page, page_num):
        self.set_title('[{}]'.format(path.basename(page.editor.image.filename)))

    def new_image(self, a, b=None):
        new_image_dialog = dialog.new_image_dialog(self)
        values = new_image_dialog.get_values()
        if values:
            if values[4]:
                mode = 'RGBA'
                color = values[2][:-1] + ',0)'
                color = color.replace('rgb', 'rgba')
            else:
                mode = 'RGB'
                color = values[2]
            img = Image.new(mode, values[1], color)
            name = values[0] if values[0] else 'untitled'
            filename = name + '.' + values[3].lower()
            self.create_tab(img, filename, False)

    def open_image(self, a, b=None):
        filename = dialog.file_dialog(self, 'open')
        if filename:
            if path.splitext(filename)[-1][1:].lower() in self.allowed_formats:
                img = Image.open(filename)
                self.create_tab(img, filename)
            else:
                error_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, 'Unable to open this file')
                error_dialog.format_secondary_text(
                    'The format of this file is not supported.')
                error_dialog.run()
                error_dialog.destroy()

    def close_tab(self, a=None, b=None, page_num=None):
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
                tab.editor.save_as()
            tab.editor.close_image()
            self.notebook.remove_page(page_num)
            dialog.destroy()
        else:
            tab.editor.close_image()
            self.notebook.remove_page(page_num)

        if self.notebook.get_n_pages() == 0:
            self.set_title('ImEditor')
            self.notebook.hide()
            self.homepage.show()
            self.sensitive_toolbar(False)

    def save(self, a, b):
        tab = self.get_tab()
        tab.editor.save()

    def save_as(self, a, b):
        tab = self.get_tab()
        tab.editor.save_as()

    def details(self, a, b):
        tab = self.get_tab()
        tab.editor.details()

    def select(self, a, b):
        tab = self.get_tab()
        tab.editor.select()

    def history(self, a, b, num):
        tab = self.get_tab()
        tab.editor.history(num)

    def copy(self, a, b):
        tab = self.get_tab()
        tab.editor.copy()

    def paste(self, a, b):
        tab = self.get_tab()
        tab.editor.paste()

    def cut(self, a, b):
        tab = self.get_tab()
        tab.editor.cut()

    def pencil(self, a, b):
        tab = self.get_tab()
        tab.editor.pencil()

    def apply_filter(self, a, b, func, params=None):
        tab = self.get_tab()
        tab.editor.apply_filter(func, params)

    def quit_app(self, a=None, b=None):
        for i in reversed(range(self.notebook.get_n_pages())):
            self.close_tab(page_num=i)
        self.app.quit()
        return False

    def about(self, a, b):
        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_logo(self.logo)
        dialog.set_program_name('ImEditor')
        dialog.set_version('0.1-dev')
        dialog.set_website('https://imeditor.github.io')
        dialog.set_authors(['Nathan Seva', 'Hugo Posnic'])
        dialog.set_comments('Simple & versatile image editor.\n\nGtk: {}.{}.{}\nPillow: {}'.format(Gtk.get_major_version(), Gtk.get_micro_version(), Gtk.get_minor_version(), pil_version))
        dialog.set_license('Distributed under the GNU GPL(v3) license. \nhttps://github.com/ImEditor/ImEditor/blob/master/LICENSE\nIcons made by Madebyoliver under CC 3.0 BY.\nhttp://www.flaticon.com/authors/madebyoliver')
        dialog.run()
        dialog.destroy()
