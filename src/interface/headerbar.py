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

        builder.add_from_resource(UI_PATH + 'menu.ui')
        self.window_menu = builder.get_object('window-menu')

        self.build_headerbar()

    def build_headerbar(self):
        self.menu_button.set_menu_model(self.window_menu)
        self.header_bar.pack_end(self.menu_button)

        # Tasks buttons
        # Pencil
        self.pencil_button = Gtk.Button.new_from_icon_name('applications-graphics-symbolic',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.pencil_button.set_action_name('win.pencil')
        self.pencil_button.set_tooltip_text(_("Pencil"))
        self.header_bar.pack_end(self.pencil_button)

        # Select
        self.select_button = Gtk.Button.new_from_icon_name('input-mouse-symbolic',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.select_button.set_action_name('win.select')
        self.select_button.set_tooltip_text(_("Selection"))
        self.header_bar.pack_end(self.select_button)

        # Toolbar
        toolbar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(toolbar_box.get_style_context(), 'linked')

        # New
        self.new_button = Gtk.Button.new_from_icon_name('document-new',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.new_button.set_action_name('win.new')
        self.new_button.set_tooltip_text(_("New"))
        toolbar_box.add(self.new_button)

        # Open
        self.open_button = Gtk.Button.new_from_icon_name('document-open',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.open_button.set_action_name('win.open')
        self.open_button.set_tooltip_text(_("Open"))
        toolbar_box.add(self.open_button)

        # Save
        self.save_button = Gtk.Button.new_from_icon_name('document-save',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.save_button.set_action_name('win.save')
        self.save_button.set_tooltip_text(_("Save"))
        toolbar_box.add(self.save_button)

        # Save as
        self.save_as_button = Gtk.Button.new_from_icon_name('document-save-as',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.save_as_button.set_action_name('win.save-as')
        self.save_as_button.set_tooltip_text(_("Save as..."))
        toolbar_box.add(self.save_as_button)

        # Undo
        self.undo_button = Gtk.Button.new_from_icon_name('edit-undo',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.undo_button.set_action_name('win.undo')
        self.undo_button.set_tooltip_text(_("Undo"))
        toolbar_box.add(self.undo_button)

        # Redo
        self.redo_button = Gtk.Button.new_from_icon_name('edit-redo',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.redo_button.set_action_name('win.redo')
        self.redo_button.set_tooltip_text(_("Redo"))
        toolbar_box.add(self.redo_button)

        # Rotate left
        self.rotate_left_button = Gtk.Button.new_from_icon_name('object-rotate-left',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.rotate_left_button.set_action_name('win.rotate-left')
        self.rotate_left_button.set_tooltip_text(_("Rotate -90°"))
        toolbar_box.add(self.rotate_left_button)

        # Rotate right
        self.rotate_right_button = Gtk.Button.new_from_icon_name('object-rotate-right',
            Gtk.IconSize.SMALL_TOOLBAR)
        self.rotate_right_button.set_action_name('win.rotate-right')
        self.rotate_right_button.set_tooltip_text(_("Rotate 90°"))
        toolbar_box.add(self.rotate_right_button)

        self.header_bar.pack_start(toolbar_box)

        self.header_bar.show_all()
