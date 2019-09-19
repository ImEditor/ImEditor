import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, GLib
from PIL import Image, __version__ as pil_version
from os import path

from .tab import Tab
from .dialog import *
from .vars import SUPPORTED_EXTENSIONS, SUPPORTED_MODES

from .headerbar import ImEditorHeaderBar

UI_PATH = '/io/github/ImEditor/ui/'

@Gtk.Template(resource_path=UI_PATH + 'window.ui')
class ImEditorWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ImEditorWindow'

    main_box = Gtk.Template.Child()
    homepage = Gtk.Template.Child()
    notebook = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs['application']

        # Init the app
        self.settings = Gio.Settings.new('io.github.ImEditor')
        self.gtk_settings = Gtk.Settings.get_default()

        self.connect('delete-event', self.quit_app)

        # Init UI objects
        self.header_bar = None
        self.shortcuts_window = None

        # Build UI
        self.build_ui()

        # Vars
        self.is_dark_mode = self.settings.get_boolean('dark-mode')
        self.filenames = list()
        self.selected_img = None  # Selected image

        # Create actions
        self.create_actions()

        self.switch_theme(self.is_dark_mode)
        self.show_all()
        self.enable_homescreen()

    def build_ui(self):
        self.header_bar = ImEditorHeaderBar()
        self.set_titlebar(self.header_bar.header_bar)

        self.notebook.set_scrollable(True)
        self.notebook.connect('switch-page', self.on_tab_switched)

    def switch_theme(self, is_dark=False):
        self.settings.set_boolean('dark-mode', is_dark)
        property = 'gtk-application-prefer-dark-theme'
        self.gtk_settings.set_property(property, is_dark)
        variant = GLib.Variant.new_boolean(is_dark)
        self.dark_mode_action.set_state(variant)
        self.is_dark_mode = is_dark

    def create_simple_action(self, action_name, callback, shortcut=None):
        action = Gio.SimpleAction.new(action_name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcut is not None:
            self.app.add_accelerator(shortcut, 'win.' + action_name, None)

    def create_actions(self):
        self.create_simple_action('quit', self.quit_app, '<Primary>q')
        self.create_simple_action('close-tab', self.close_tab, '<Primary>w')
        self.create_simple_action('shortcuts', self.shortcuts)
        self.create_simple_action('about', self.about)

        # Pencil
        self.pencil_action = Gio.SimpleAction.new('pencil', None)
        self.pencil_action.connect('activate', self.pencil)
        self.add_action(self.pencil_action)

        # Select
        self.select_action = Gio.SimpleAction.new('select', None)
        self.select_action.connect('activate', self.select)
        self.add_action(self.select_action)

        # New
        self.new_action = Gio.SimpleAction.new('new', None)
        self.new_action.connect('activate', self.new_image)
        self.add_action(self.new_action)
        self.app.add_accelerator('<Primary>n', 'win.new', None)

        # Open
        self.open_action = Gio.SimpleAction.new('open', None)
        self.open_action.connect('activate', self.open_image)
        self.add_action(self.open_action)
        self.app.add_accelerator('<Primary>o', 'win.open', None)

        # Save
        self.save_action = Gio.SimpleAction.new('save', None)
        self.save_action.connect('activate', lambda *args:self.get_tab().editor.save())
        self.add_action(self.save_action)
        self.app.add_accelerator('<Primary>s', 'win.save', None)

        # Save as
        self.save_as_action = Gio.SimpleAction.new('save-as', None)
        self.save_as_action.connect('activate', lambda *args:self.get_tab().editor.save_as())
        self.add_action(self.save_as_action)
        self.app.add_accelerator('<Primary><Shift>s', 'win.save-as', None)

        # Undo
        self.undo_action = Gio.SimpleAction.new('undo', None)
        self.undo_action.connect('activate', lambda *args:self.get_tab().editor.undo())
        self.add_action(self.undo_action)
        self.app.add_accelerator('<Primary>z', 'win.undo', None)

        # Redo
        self.redo_action = Gio.SimpleAction.new('redo', None)
        self.redo_action.connect('activate', lambda *args:self.get_tab().editor.redo())
        self.add_action(self.redo_action)
        self.app.add_accelerator('<Primary>y', 'win.redo', None)

        # Rotate left
        self.rotate_left_action = Gio.SimpleAction.new('rotate-left', None)
        self.rotate_left_action.connect('activate', self.apply_filter, 'rotate', -90)
        self.add_action(self.rotate_left_action)

        # Rotate right
        self.rotate_right_action = Gio.SimpleAction.new('rotate-right', None)
        self.rotate_right_action.connect('activate', self.apply_filter, 'rotate', 90)
        self.add_action(self.rotate_right_action)

        # Copy
        self.copy_action = Gio.SimpleAction.new('copy', None)
        self.copy_action.connect('activate', lambda *args:self.get_tab().editor.copy())
        self.add_action(self.copy_action)
        self.app.add_accelerator('<Primary>c', 'win.copy', None)

        # Paste
        self.paste_action = Gio.SimpleAction.new('paste', None)
        self.paste_action.connect('activate', lambda *args:self.get_tab().editor.paste())
        self.add_action(self.paste_action)
        self.app.add_accelerator('<Primary>v', 'win.paste', None)

        # Cut
        self.cut_action = Gio.SimpleAction.new('cut', None)
        self.cut_action.connect('activate', lambda *args:self.get_tab().editor.cut())
        self.add_action(self.cut_action)
        self.app.add_accelerator('<Primary>x', 'win.cut', None)

        # Zoom -
        self.zoom_minus_action = Gio.SimpleAction.new('zoom-minus', None)
        self.zoom_minus_action.connect('activate', self.zoom, -1)
        self.add_action(self.zoom_minus_action)
        self.app.add_accelerator('<Primary>minus', 'win.zoom-minus', None)

        # Zoom +
        self.zoom_plus_action = Gio.SimpleAction.new('zoom-plus', None)
        self.zoom_plus_action.connect('activate', self.zoom, 1)
        self.add_action(self.zoom_plus_action)
        self.app.add_accelerator('<Primary>plus', 'win.zoom-plus', None)

        # Details
        self.details_action = Gio.SimpleAction.new('details', None)
        self.details_action.connect('activate', lambda *args:self.get_tab().editor.details())
        self.add_action(self.details_action)

        # Dark mode
        self.dark_mode_action = Gio.SimpleAction.new_stateful('dark-mode',
            None, GLib.Variant.new_boolean(self.is_dark_mode))
        self.dark_mode_action.connect('activate', self.toggle_dark_theme)
        self.add_action(self.dark_mode_action)

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
        self.crop_action.connect('activate', lambda *args:self.get_tab().editor.crop())
        self.add_action(self.crop_action)

    def set_window_title(self, tab):
        title = '[{}] - {}'.format(path.basename(tab.editor.image.filename),
            'ImEditor')
        if tab.zoom_level != 100:
            title += ' - {}%'.format(tab.zoom_level)
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
            self.set_title('ImEditor')
            self.notebook.hide()
            self.homepage.show()
            self.enable_toolbar(False)
        else:
            self.homepage.hide()
            self.notebook.show()
            self.enable_toolbar()

    def new_image(self, a, b):
        """Launch the new image dialog"""
        dialog = new_image_dialog(self)
        values = dialog.get_values()
        if values:
            if values[3]:  # if transparent background
                color = 'rgba(255, 255, 255, 0)'
                mode = 'RGBA'
            else:
                color = values[2]
                mode = 'RGB'
            img = Image.new(mode, values[1], color)
            name = values[0] if values[0] else _("untitled")
            filename = name + '.' + values[4].lower()
            self.create_tab(img, filename)

    def open_image(self, a=None, b=None, filename=None):
        """Open an existing image"""
        if not filename:
            filename = file_dialog(self, 'open')
        if not filename:
            return
        if not path.isfile(filename):
            message_dialog(self, 'error', _("Unable to open this image"),
                _("This image doesn't exists. Please verify the path."))
            return
        if filename not in self.filenames: # is image already opened?
            if path.splitext(filename)[-1][1:].lower() in SUPPORTED_EXTENSIONS:
                img = Image.open(filename)
                if img.mode in SUPPORTED_MODES:
                    self.create_tab(img, filename, True)
                    self.filenames.append(filename)
                else:
                    message_dialog(self, 'error', _("Unable to open this image"),
                        _("The mode of this image is not supported."))
            else:
                message_dialog(self, 'error', _("Unable to open this file"),
                    _("The format of this file is not supported."))
        else:
            message_dialog(self, 'warning', _("Already open"),
                _("This image is already opened in ImEditor."))

    def get_tab(self, page_num=None):
        """Get tab by its num or get the current one"""
        if page_num is None:
            page_num = self.notebook.get_current_page()
        return self.notebook.get_nth_page(page_num)

    def create_tab(self, img, filename, saved=False):
        """Instantiate a new tab"""
        tab = Tab(self, img, filename, saved)
        page_num = self.notebook.get_current_page() + 1
        nb_tabs = self.notebook.get_n_pages()
        if nb_tabs == 0:
            self.enable_homescreen(False)
        self.notebook.insert_page(tab, tab.tab_label, page_num)
        self.notebook.set_tab_reorderable(tab, True)
        self.notebook.set_current_page(page_num)
        self.switch_show_tabs()

    def close_tab(self, a=None, b=None, page_num=None):
        """Close tab by user action"""
        if self.notebook.get_n_pages() == 0:
            return
        tab = self.get_tab(page_num)
        if page_num is None:
            page_num = self.notebook.page_num(tab)
        if not tab.editor.image.saved or \
           not path.exists(tab.editor.image.filename):  # if image is not saved
            description = _("Do you want to save the changes of the \"{}\" image before closing it?") \
                .format(path.basename(tab.editor.image.filename))
            response = message_dialog(self, 'question', \
                _("There are unsaved changes to this image"),
                description)
            if response == Gtk.ResponseType.YES:
                tab.editor.save_as()
                self.close_tab_by_id(tab, page_num)
            elif response == Gtk.ResponseType.NO:
                self.close_tab_by_id(tab, page_num)
        else:
            self.close_tab_by_id(tab, page_num)

        if self.notebook.get_n_pages() == 0:  # re-display the homescreen
            self.enable_homescreen(True)

        self.switch_show_tabs()

    def close_tab_by_id(self, tab, page_num):
        """Close tab by its id"""
        tab.editor.close_image()
        if path.isfile(tab.editor.image.filename):
            self.filenames.remove(tab.editor.image.filename)
        self.notebook.remove_page(page_num)

    def switch_show_tabs(self):
        show_tabs = self.notebook.get_n_pages() > 1
        self.notebook.set_show_tabs(show_tabs)

    def on_tab_switched(self, notebook, tab, page_num):
        self.set_window_title(tab)
        self.select_current_tool(tab)

    def select_current_tool(self, tab):
        if tab.editor.task == 0:
            self.select(tab=tab)
        elif tab.editor.task == 2:
            self.pencil(tab=tab)

    def select(self, a=None, b=None, tab=None):
        self.header_bar.select_button.set_sensitive(False)
        self.header_bar.pencil_button.set_sensitive(True)
        if not tab:
            tab = self.get_tab()
        tab.editor.change_task()
        tab.enable_sidebar(False)

    def pencil(self, a=None, b=None, tab=None):
        self.header_bar.pencil_button.set_sensitive(False)
        self.header_bar.select_button.set_sensitive(True)
        if not tab:
            tab = self.get_tab()
        tab.editor.change_task('draw')
        tab.enable_sidebar()

    def apply_filter(self, a, b, func, value=None):
        tab = self.get_tab()
        tab.editor.apply_filter(func, value)

    def apply_filter_dialog(self, a, b, func, params=None):
        tab = self.get_tab()
        tab.editor.apply_filter_dialog(func, params)

    def zoom(self, a, b, value):
        tab = self.get_tab()
        tab.zoom(value)

    def toggle_dark_theme(self, *args):
        self.switch_theme(not self.is_dark_mode)

    def shortcuts(self, *args):
        if self.shortcuts_window is not None:
            self.shortcuts_window.destroy()
        builder = Gtk.Builder().new_from_resource( \
                                '/io/github/ImEditor/ui/shortcuts.ui')
        self.shortcuts_window = builder.get_object('shortcuts-window')
        self.shortcuts_window.present()

    def about(self, *args):
        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_logo_icon_name('io.github.ImEditor')
        dialog.set_program_name('ImEditor')
        dialog.set_version('0.9.3')
        dialog.set_website('https://imeditor.github.io')
        dialog.set_authors(['Nathan Seva', 'Hugo Posnic'])
        gtk_version = '{}.{}.{}'.format(Gtk.get_major_version(),
            Gtk.get_minor_version(), Gtk.get_micro_version())
        dialog.set_comments('{}\n\n' \
            'Gtk: {}\nPillow: {}'.format(_("Simple & versatile image editor"), gtk_version,
            pil_version))
        text = _("Distributed under the GNU GPL(v3) license.\n")
        text += 'https://github.com/ImEditor/ImEditor/blob/master/LICENSE\n'
        dialog.set_license(text)
        dialog.run()
        dialog.destroy()

    def quit_app(self, *args):
        """Close all tabs to be sure they are saved"""
        for i in reversed(range(self.notebook.get_n_pages())):
            self.close_tab(page_num=i)
        self.app.quit()
