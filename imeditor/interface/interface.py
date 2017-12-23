#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
from PIL import Image, __version__ as pil_version
from os import path

from interface.tab import Tab
from interface import dialog


class Interface(Gtk.ApplicationWindow):
    def __init__(self, app):
        self.program_title = 'ImEditor'
        self.program_description = 'Simple & versatile image editor'
        Gtk.Window.__init__(self, title=self.program_title, application=app)
        self.connect('delete-event', self.quit_app)
        self.app = app
        self.set_default_size(950, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.bpath = path.dirname(path.dirname(path.abspath(__file__))) + '/'
        self.logo = GdkPixbuf.Pixbuf.new_from_file(
                        '{}assets/imeditor.png'.format(self.bpath))
        self.set_icon(self.logo)

        # Header Bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.program_title
        hb.props.subtitle = self.program_description
        self.set_titlebar(hb)

        # Menu
        menu_button = Gtk.MenuButton()
        menu_button.set_image(Gtk.Image.new_from_icon_name('open-menu-symbolic',
            Gtk.IconSize.MENU))
        menu_model = Gio.Menu()
        menu_model.append('Zoom -', 'win.zoom-minus')
        menu_model.append('Zoom +', 'win.zoom-plus')
        menu_model.append('Cut', 'win.cut')
        menu_model.append('Copy', 'win.copy')
        menu_model.append('Paste', 'win.paste')
        menu_model.append('Cut', 'win.cut')
        submenu_1 = Gio.Menu()
        submenu_1.append('Black & white', 'win.black-and-white')
        submenu_1.append('Negative', 'win.negative')
        submenu_1.append('Red', 'win.red')
        submenu_1.append('Green', 'win.green')
        submenu_1.append('Blue', 'win.blue')
        submenu_1.append('Grayscale', 'win.grayscale')
        submenu_1.append('Brightness', 'win.brightness')
        menu_model.append_submenu('Filters', submenu_1)
        submenu_2 = Gio.Menu()
        submenu_2.append('Horizontal mirror', 'win.horizontal-mirror')
        submenu_2.append('Vertical mirror', 'win.vertical-mirror')
        submenu_2.append('Crop', 'win.crop')
        menu_model.append_submenu('Operations', submenu_2)
        menu_model.append('Image details', 'win.details')
        menu_model.append('About', 'win.about')
        menu_button.set_menu_model(menu_model)
        hb.pack_end(menu_button)

        # Actions
        # Close button of tabs
        self.close_action = Gio.SimpleAction.new('close-tab', None)
        self.close_action.connect('activate', self.close_tab)
        self.add_action(self.close_action)
        app.add_accelerator('<Primary>w', 'win.close-tab', None)

        # Pencil
        self.pencil_action = Gio.SimpleAction.new('pencil', None)
        self.pencil_action.connect('activate', self.pencil)
        self.add_action(self.pencil_action)
        self.pencil_button = Gtk.Button()
        self.pencil_button.set_image(Gtk.Image.new_from_file(
                                    '{}assets/pencil.png'.format(self.bpath)))
        self.pencil_button.set_action_name('win.pencil')
        hb.pack_end(self.pencil_button)

        # Select
        self.select_action = Gio.SimpleAction.new('select', None)
        self.select_action.connect('activate', self.select)
        self.add_action(self.select_action)
        self.select_button = Gtk.Button()
        self.select_button.set_image(Gtk.Image.new_from_file(
                                    '{}assets/select.png'.format(self.bpath)))
        self.select_button.set_action_name('win.select')
        hb.pack_end(self.select_button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), 'linked')

        # New
        self.new_action = Gio.SimpleAction.new('new', None)
        self.new_action.connect('activate', self.new_image)
        self.add_action(self.new_action)
        app.add_accelerator('<Primary>n', 'win.new', None)
        self.new_button = Gtk.Button.new_from_icon_name('document-new',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.new_button.set_action_name('win.new')
        box.add(self.new_button)

        # Open
        self.open_action = Gio.SimpleAction.new('open', None)
        self.open_action.connect('activate', self.open_image)
        self.add_action(self.open_action)
        app.add_accelerator('<Primary>o', 'win.open', None)
        self.open_button = Gtk.Button.new_from_icon_name('document-open',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.open_button.set_action_name('win.open')
        box.add(self.open_button)

        # Save
        self.save_action = Gio.SimpleAction.new('save', None)
        self.save_action.connect('activate', self.save)
        self.add_action(self.save_action)
        app.add_accelerator('<Primary>s', 'win.save', None)
        self.save_button = Gtk.Button.new_from_icon_name('document-save',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.save_button.set_action_name('win.save')
        box.add(self.save_button)

        # Save as
        self.save_as_action = Gio.SimpleAction.new('save-as', None)
        self.save_as_action.connect('activate', self.save_as)
        self.add_action(self.save_as_action)
        self.save_as_button = Gtk.Button.new_from_icon_name('document-save-as',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.save_as_button.set_action_name('win.save-as')
        box.add(self.save_as_button)

        # Undo
        self.undo_action = Gio.SimpleAction.new('undo', None)
        self.undo_action.connect('activate', self.undo)
        self.add_action(self.undo_action)
        app.add_accelerator('<Primary>z', 'win.undo', None)
        self.undo_button = Gtk.Button.new_from_icon_name('edit-undo',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.undo_button.set_action_name('win.undo')
        box.add(self.undo_button)

        # Redo
        self.redo_action = Gio.SimpleAction.new('redo', None)
        self.redo_action.connect('activate', self.redo)
        self.add_action(self.redo_action)
        app.add_accelerator('<Primary>y', 'win.redo', None)
        self.redo_action_button = Gtk.Button.new_from_icon_name('edit-redo',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.redo_action_button.set_action_name('win.redo')
        box.add(self.redo_action_button)

        # Rotate left
        self.rotate_left_action = Gio.SimpleAction.new('rotate-left', None)
        self.rotate_left_action.connect('activate', self.apply_filter, 'rotate', -90)
        self.add_action(self.rotate_left_action)
        self.rotate_left_button = Gtk.Button.new_from_icon_name('object-rotate-left',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.rotate_left_button.set_action_name('win.rotate-left')
        box.add(self.rotate_left_button)

        # Rotate right
        self.rotate_right_action = Gio.SimpleAction.new('rotate-right', None)
        self.rotate_right_action.connect('activate', self.apply_filter, 'rotate', 90)
        self.add_action(self.rotate_right_action)
        self.rotate_right_button = Gtk.Button.new_from_icon_name('object-rotate-right',
            Gtk.IconSize.SMALL_TOOLBAR)
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

        # Zoom -
        self.zoom_minus_action = Gio.SimpleAction.new('zoom-minus', None)
        self.zoom_minus_action.connect('activate', self.zoom, -1)
        self.add_action(self.zoom_minus_action)
        app.add_accelerator('<Primary>minus', 'win.zoom-minus', None)

        # Zoom +
        self.zoom_plus_action = Gio.SimpleAction.new('zoom-plus', None)
        self.zoom_plus_action.connect('activate', self.zoom, 1)
        self.add_action(self.zoom_plus_action)
        app.add_accelerator('<Primary>equal', 'win.zoom-plus', None)

        # Details
        self.details_action = Gio.SimpleAction.new('details', None)
        self.details_action.connect('activate', self.details)
        self.add_action(self.details_action)

        # About
        self.about_action = Gio.SimpleAction.new('about', None)
        self.about_action.connect('activate', self.about)
        self.add_action(self.about_action)

        # Filters
        self.black_and_white_action = Gio.SimpleAction.new('black-and-white', None)
        self.black_and_white_action.connect('activate', self.apply_filter_dialog,
            'black_white', ('Black & white', [0, 255]))
        self.add_action(self.black_and_white_action)

        self.negative_action = Gio.SimpleAction.new('negative', None)
        self.negative_action.connect('activate', self.apply_filter, 'negative')
        self.add_action(self.negative_action)

        self.red_action = Gio.SimpleAction.new('red', None)
        self.red_action.connect('activate', self.apply_filter, 'red')
        self.add_action(self.red_action)

        self.green_action = Gio.SimpleAction.new('green', None)
        self.green_action.connect('activate', self.apply_filter, 'green')
        self.add_action(self.green_action)

        self.blue_action = Gio.SimpleAction.new('blue', None)
        self.blue_action.connect('activate', self.apply_filter, 'blue')
        self.add_action(self.blue_action)

        self.grayscale_action = Gio.SimpleAction.new('grayscale', None)
        self.grayscale_action.connect('activate', self.apply_filter, 'grayscale')
        self.add_action(self.grayscale_action)

        self.brightness_action = Gio.SimpleAction.new('brightness', None)
        self.brightness_action.connect('activate', self.apply_filter_dialog,
            'brightness', ('Brightness', [-255, 255]))
        self.add_action(self.brightness_action)

        # Operations
        self.horizontal_mirror_action = Gio.SimpleAction.new('horizontal-mirror', None)
        self.horizontal_mirror_action.connect('activate', self.apply_filter,
            'horizontal_mirror')
        self.add_action(self.horizontal_mirror_action)

        self.vertical_mirror_action = Gio.SimpleAction.new('vertical-mirror', None)
        self.vertical_mirror_action.connect('activate', self.apply_filter,
            'vertical_mirror')
        self.add_action(self.vertical_mirror_action)

        self.crop_action = Gio.SimpleAction.new('crop', None)
        self.crop_action.connect('activate', self.crop)
        self.add_action(self.crop_action)

        hb.pack_start(box)

        # Homepage
        self.homepage = Gtk.Grid(row_spacing=20, column_spacing=20,
            margin_top=120, margin_bottom=120)
        self.homepage.set_halign(Gtk.Align.CENTER)
        label = Gtk.Label()
        label.set_markup('<span size="xx-large">What do you want to do?</span>')
        new_button = Gtk.Button('Create a new image', always_show_image=True)
        new_button.set_image(Gtk.Image.new_from_icon_name('document-new',
            Gtk.IconSize.BUTTON))
        new_button.set_action_name('win.new')
        open_button = Gtk.Button('Open an existing image', always_show_image=True)
        open_button.set_image(Gtk.Image.new_from_icon_name('document-open',
            Gtk.IconSize.BUTTON))
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

        self.show_all()
        self.enable_homescreen()

        # Cursors
        display = Gdk.Display.get_default()
        self.cursors = {
            'default': Gdk.Cursor.new_from_name(display, 'default'),
            'draw': Gdk.Cursor.new_for_display(display, Gdk.CursorType.PENCIL),
            'move': Gdk.Cursor.new_from_name(display, 'move')
        }

        # Settings
        self.allowed_formats = ('bmp', 'ico', 'jpeg', 'jpg', 'png', 'webp')
        self.allowed_modes = ('RGB', 'RGBA')

        # Vars
        self.filenames = list()

    def set_window_title(self, tab):
        title = '[{}] - {}'.format(path.basename(tab.editor.image.filename),
            self.program_title)
        if tab.zoom_level != 100:
            title += '- {}%'.format(tab.zoom_level)
        self.set_title(title)

    def enable_toolbar(self, enable=True):
        """Set state of actions (depending on whether an image is open)"""
        actions = ('pencil', 'select', 'save', 'save_as', 'undo', 'redo',
            'rotate_left', 'rotate_right', 'copy', 'paste', 'cut', 'crop',
            'details', 'black_and_white', 'negative', 'red', 'green', 'blue',
            'grayscale', 'brightness', 'vertical_mirror', 'horizontal_mirror',
            'zoom_minus', 'zoom_plus')
        for action in actions:
            getattr(self, action + '_action').set_enabled(enable)

    def enable_homescreen(self, enable=True):
        if enable:
            self.set_title(self.program_title)
            self.notebook.hide()
            self.homepage.show()
            self.enable_toolbar(False)
        else:
            self.homepage.hide()
            self.notebook.show()
            self.enable_toolbar()

    def new_image(self, a, b):
        """Launch the new image dialog"""
        new_image_dialog = dialog.new_image_dialog(self)
        values = new_image_dialog.get_values()
        if values:
            if values[3]:  # if transparent background
                color = 'rgba(255, 255, 255, 0)'
                mode = 'RGBA'
            else:
                color = values[2]
                mode = 'RGB'
            img = Image.new(mode, values[1], color)
            name = values[0] if values[0] else 'untitled'
            filename = name + '.' + values[4].lower()
            self.create_tab(img, filename, False)

    def open_image(self, a, b):
        """Open an existing image"""
        filename = dialog.file_dialog(self, 'open')
        if not filename:
            return
        if filename not in self.filenames: # is image already opened ?
            if path.splitext(filename)[-1][1:].lower() in self.allowed_formats:
                img = Image.open(filename)
                if img.mode in self.allowed_modes:
                    self.create_tab(img, filename)
                    self.filenames.append(filename)
                else:
                    dialog.message_dialog(self, 'error', 'Unable to open this image',
                        'The mode of this image is not supported.')
            else:
                dialog.message_dialog(self, 'error', 'Unable to open this file',
                    'The format of this file is not supported.')
        else:
            dialog.message_dialog(self, 'warning', 'Already open',
                'This image is already opened in ImEditor.')

    def get_tab(self, page_num=None):
        """Get tab by its num or get the current one"""
        if not page_num:
            page_num = self.notebook.get_current_page()
        return self.notebook.get_nth_page(page_num)

    def create_tab(self, img, filename, saved=True):
        """Instantiate a new tab"""
        tab = Tab(self, img, filename, saved)
        page_num = self.notebook.get_current_page() + 1
        nb_tabs = self.notebook.get_n_pages()
        if nb_tabs == 0:
            self.enable_homescreen(False)
        self.notebook.insert_page(tab, tab.tab_label, page_num)
        self.notebook.set_current_page(page_num)

    def close_tab(self, a=None, b=None, page_num=None):
        """Close tab by user action"""
        tab = self.get_tab(page_num)
        if not page_num:
            page_num = self.notebook.page_num(tab)
        if not tab.editor.image.saved:  # if image is not saved
            title = 'Do you want to save the changes to the « {} » image before closing it?'.format(path.basename(tab.editor.image.filename))
            response = dialog.message_dialog(self, 'question', title,
                'If you don\'t save it, the changes made will be permanently lost.')
            if response == Gtk.ResponseType.YES:
                tab.editor.save_as()
                self.close_tab_by_id(tab, page_num)
            elif response == Gtk.ResponseType.NO:
                self.close_tab_by_id(tab, page_num)
        else:
            self.close_tab_by_id(tab, page_num)

        if self.notebook.get_n_pages() == 0:  # re-display the homescreen
            self.enable_homescreen(True)

    def close_tab_by_id(self, tab, page_num):
        """Close tab by its id"""
        tab.editor.close_image()
        if path.isfile(tab.editor.image.filename):
            self.filenames.remove(tab.editor.image.filename)
        self.notebook.remove_page(page_num)

    def on_tab_switched(self, notebook, tab, page_num):
        self.set_window_title(tab)
        self.select_current_tool(tab)

    def save(self, a, b):
        tab = self.get_tab()
        tab.editor.save()

    def save_as(self, a, b):
        tab = self.get_tab()
        tab.editor.save_as()

    def details(self, a, b):
        tab = self.get_tab()
        tab.editor.details()

    def undo(self, a, b):
        tab = self.get_tab()
        tab.editor.undo()

    def redo(self, a, b):
        tab = self.get_tab()
        tab.editor.redo()

    def zoom(self, a, b, value):
        tab = self.get_tab()
        tab.zoom(value)

    def copy(self, a, b):
        tab = self.get_tab()
        tab.editor.copy()

    def paste(self, a, b):
        tab = self.get_tab()
        tab.editor.paste()

    def cut(self, a, b):
        tab = self.get_tab()
        tab.editor.cut()

    def crop(self, a, b):
        tab = self.get_tab()
        tab.editor.crop()

    def select(self, a=None, b=None, tab=None):
        self.select_button.set_sensitive(False)
        self.pencil_button.set_sensitive(True)
        if not tab:
            tab = self.get_tab()
        tab.editor.change_task()
        tab.enable_sidebar(False)

    def pencil(self, a=None, b=None, tab=None):
        self.pencil_button.set_sensitive(False)
        self.select_button.set_sensitive(True)
        if not tab:
            tab = self.get_tab()
        tab.editor.change_task('pencil')
        tab.enable_sidebar()

    def select_current_tool(self, tab):
        if tab.editor.task == 0:
            self.select(tab=tab)
        elif tab.editor.task == 2:
            self.pencil(tab=tab)

    def apply_filter(self, a, b, func, value=None):
        tab = self.get_tab()
        tab.editor.apply_filter(func, value)

    def apply_filter_dialog(self, a, b, func, params=None):
        tab = self.get_tab()
        tab.editor.apply_filter_dialog(func, params)

    def quit_app(self, a, b):
        """Close all tabs to be sure they are saved"""
        for i in reversed(range(self.notebook.get_n_pages())):
            self.close_tab(page_num=i)
        self.app.quit()
        return False

    def about(self, a, b):
        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_logo(self.logo)
        dialog.set_program_name(self.program_title)
        dialog.set_version('0.5.1')
        dialog.set_website('https://imeditor.github.io')
        dialog.set_authors(['Nathan Seva', 'Hugo Posnic'])
        gtk_version = '{}.{}.{}'.format(Gtk.get_major_version(),
            Gtk.get_micro_version(), Gtk.get_minor_version())
        dialog.set_comments('{}\n\n' \
            'Gtk: {}\nPillow: {}'.format(self.program_description, gtk_version,
            pil_version))
        text = 'Distributed under the GNU GPL(v3) license.\n'
        text += 'https://github.com/ImEditor/ImEditor/blob/master/LICENSE\n'
        text += 'Icons made by Madebyoliver under CC 3.0 BY.\n'
        text += 'http://www.flaticon.com/authors/madebyoliver'
        dialog.set_license(text)
        dialog.run()
        dialog.destroy()
