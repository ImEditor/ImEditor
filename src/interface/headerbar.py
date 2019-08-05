import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

UI_PATH = '/io/github/ImEditor/ui/'

class ImEditorHeaderBar():
    __gtype_name__ = 'ImEditorHeaderBar'

    def __init__(self):
        builder = Gtk.Builder.new_from_resource(UI_PATH + 'headerbar.ui')
        self.header_bar = builder.get_object('header_bar')
        self.menu_button = builder.get_object('menu_button')

        self.select_button = builder.get_object('select_button')
        self.pencil_button = builder.get_object('pencil_button')

        builder.add_from_resource(UI_PATH + 'menu.ui')
        self.window_menu = builder.get_object('window-menu')

        self.menu_button.set_menu_model(self.window_menu)

