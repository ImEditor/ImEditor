#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from os import path

from editor.editor import Editor
from interface.tools import pil_to_pixbuf, SpinButton


class Tab(Gtk.Box):
    def __init__(self, win, img, filename, saved):
        Gtk.Box.__init__(self)
        self.win = win

        self.editor = Editor(self.win, self, img, filename, saved)

        # Image
        self.img_widget = Gtk.Image.new_from_pixbuf(pil_to_pixbuf(img))

        event_box = Gtk.EventBox()
        event_box.set_events(Gdk.EventMask.BUTTON1_MOTION_MASK)
        event_box.connect('button-press-event', self.editor.handle_event, 'press')
        event_box.connect('motion-notify-event', self.editor.handle_event, 'move')
        event_box.connect('button-release-event', self.editor.handle_event, 'release')
        event_box.add(self.img_widget)

        frame = Gtk.Frame(hexpand=True, vexpand=True)
        frame.set_halign(Gtk.Align.CENTER)
        frame.set_valign(Gtk.Align.CENTER)
        frame.set_name('TabFrame')
        frame.add(event_box)
        style_provider = Gtk.CssProvider()
        css = b"""
        #TabFrame {
            background: url('assets/transparent.png');
        }
        """
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(frame)

        # Sidebar
        self.sidebar_frame = Gtk.Frame()

        # Pencil
        self.pencil_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, border_width=25, spacing=10)
        pencil_label = Gtk.Label('<b>Pencil</b>', use_markup=True)
        shape_pencil_label = Gtk.Label('Shape')
        pencil_shape_combo = Gtk.ComboBoxText()
        pencil_shape_combo.set_entry_text_column(0)
        shapes = ['Ellipse', 'Rectangle']
        for shape in shapes:
            pencil_shape_combo.append_text(shape)
        pencil_shape_combo.set_active(0)
        pencil_shape_combo.connect('changed', self.on_pencil_shape_changed)
        color_pencil_label = Gtk.Label('Color')
        pencil_color_button = Gtk.ColorButton()
        pencil_color_button.set_use_alpha(False)
        pencil_color_button.set_rgba(Gdk.RGBA(0, 0, 0, 1))
        pencil_color_button.connect('color-set', self.on_pencil_color_changed)
        size_pencil_label = Gtk.Label('Size')
        pencil_size_spin = SpinButton(8, 1, 1000, 1, 2)
        pencil_size_spin.connect('value-changed', self.on_pencil_size_changed)
        self.pencil_box.add(pencil_label)
        self.pencil_box.add(shape_pencil_label)
        self.pencil_box.add(pencil_shape_combo)
        self.pencil_box.add(color_pencil_label)
        self.pencil_box.add(pencil_color_button)
        self.pencil_box.add(size_pencil_label)
        self.pencil_box.add(pencil_size_spin)

        self.sidebar_frame.add(self.pencil_box)

        # Main Box
        self.add(scrolled_window)
        self.add(self.sidebar_frame)

        self.tab_label = TabLabel(path.basename(filename), img)
        self.tab_label.button.connect('clicked', self.on_close_button_clicked)

        self.show_all()
        self.sidebar_frame.hide()
        self.pencil_box.hide()

    def update_image(self, img):
        self.tab_label.set_icon(img)
        self.img_widget.set_from_pixbuf(pil_to_pixbuf(img))

    def enable_sidebar(self, enable=True):
        if enable:
            self.sidebar_frame.show()
            if self.editor.task == 0:
                self.pencil_box.show()
        else:
            self.sidebar_frame.hide()

    def on_pencil_shape_changed(self, button):
        self.editor.pencil_shape = button.get_active_text().lower()

    def on_pencil_color_changed(self, button):
        self.editor.pencil_color = button.get_rgba().to_string()

    def on_pencil_size_changed(self, button):
        self.editor.pencil_size = button.get_value_as_int()

    def on_close_button_clicked(self, button):
        page_num = self.win.notebook.page_num(self)
        self.win.close_tab(page_num)


class TabLabel(Gtk.Box):
    """Define the label on the tab."""
    def __init__(self, title, img):
        Gtk.Box.__init__(self)
        self.set_spacing(5)

        # Preview of image
        self.icon = Gtk.Image()
        self.set_icon(img)

        # Title
        self.label = Gtk.Label()
        self.set_title(title)

        # Close button
        self.button = Gtk.Button()
        self.button.set_action_name('win.close-tab')
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        self.button.add(Gtk.Image.new_from_icon_name('window-close', Gtk.IconSize.MENU))

        self.add(self.icon)
        self.add(self.label)
        self.add(self.button)

        self.show_all()

    def set_title(self, title):
        max_size = 30
        if len(title) > max_size:
            title = title[:max_size - 3] + "..."
        self.label.set_text(title)

    def set_icon(self, img):
        icon = img.copy()
        icon.thumbnail((24, 24))
        self.icon.set_from_pixbuf(pil_to_pixbuf(icon))
