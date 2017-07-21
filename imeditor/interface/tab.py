#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk

from editor.editor import Editor
from interface.tools import pil_to_pixbuf, SpinButton


class Tab(Gtk.Box):
    def __init__(self, win, img, title, filename, saved):
        Gtk.Box.__init__(self)
        self.win = win
        self.editor = Editor(self.win, self, img, filename, saved)

        # Image

        pixbuf = pil_to_pixbuf(img)
        self.img_widget = Gtk.Image.new_from_pixbuf(pixbuf)

        event_box = Gtk.EventBox()
        event_box.set_events(Gdk.EventMask.BUTTON1_MOTION_MASK)
        event_box.connect('button-press-event', self.editor.press_task)
        event_box.connect('motion-notify-event', self.editor.move_task)
        event_box.connect('button-release-event', self.editor.release_task)
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
        self.pencil_grid = Gtk.Grid(row_spacing=20, column_spacing=20, border_width=15)
        pencil_label = Gtk.Label('<b>Pencil</b>', use_markup=True)
        self.pencil_grid.attach(pencil_label, 0, 0, 2, 1)
        shape_pencil_label = Gtk.Label('Shape')
        self.pencil_grid.attach(shape_pencil_label, 0, 1, 1, 1)
        pencil_shape_combo = Gtk.ComboBoxText()
        pencil_shape_combo.set_entry_text_column(0)
        shapes = ['Ellipse', 'Rectangle']
        for shape in shapes:
            pencil_shape_combo.append_text(shape)
        pencil_shape_combo.set_active(0)
        pencil_shape_combo.connect('changed', self.on_pencil_shape_changed)
        self.pencil_grid.attach(pencil_shape_combo, 1, 1, 2, 1)
        color_pencil_label = Gtk.Label('Color')
        self.pencil_grid.attach(color_pencil_label, 0, 2, 1, 1)
        pencil_color_button = Gtk.ColorButton()
        pencil_color_button.set_use_alpha(False)
        pencil_color_button.set_rgba(Gdk.RGBA(0, 0, 0, 1))
        pencil_color_button.connect('color-set', self.on_pencil_color_changed)
        self.pencil_grid.attach(pencil_color_button, 1, 2, 1, 1)
        size_pencil_label = Gtk.Label('Size')
        self.pencil_grid.attach(size_pencil_label, 0, 3, 1, 1)
        pencil_size_spin = SpinButton(8, 1, 1000, 1, 2)
        self.pencil_grid.attach(pencil_size_spin, 1, 3, 1, 1)
        pencil_size_spin.connect('value-changed', self.on_pencil_size_changed)
        self.sidebar_frame.add(self.pencil_grid)

        # Main Box

        self.add(scrolled_window)
        self.add(self.sidebar_frame)

        self.tab_label = TabLabel(title, img)
        self.tab_label.connect('close-clicked', self.on_close_button_clicked)

        self.show_all()
        self.sidebar_frame.hide()
        self.pencil_grid.hide()

    def update_image(self, new_img):
        self.tab_label.set_icon(new_img)
        pixbuf = pil_to_pixbuf(new_img)
        self.img_widget.set_from_pixbuf(pixbuf)

    def enable_sidebar(self, enable):
        if enable:
            self.sidebar_frame.show()
            if self.editor.task == 0:
                self.pencil_grid.show()
        else:
            self.sidebar_frame.hide()

    def on_pencil_shape_changed(self, button):
        self.editor.pencil_shape = button.get_active_text().lower()

    def on_pencil_color_changed(self, button):
        self.editor.pencil_color = button.get_rgba().to_string()

    def on_pencil_size_changed(self, button):
        self.editor.pencil_size = button.get_value_as_int()

    def on_close_button_clicked(self, _):
        page_num = self.win.notebook.page_num(self)
        self.win.close_tab(page_num=page_num)


class TabLabel(Gtk.Box):
    """Define the label on the tab."""
    __gsignals__ = {'close-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())}
    def __init__(self, title, img):
        Gtk.Box.__init__(self)
        self.set_spacing(5)

        # Preview of image
        self.icon_widget = Gtk.Image()
        self.set_icon(img)

        # Title
        self.label = Gtk.Label()
        self.set_title(title)

        # Close button
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.add(Gtk.Image.new_from_icon_name('window-close', Gtk.IconSize.MENU))
        button.connect('clicked', self.on_close_button_clicked)

        self.add(self.icon_widget)
        self.add(self.label)
        self.add(button)

        self.show_all()

    def set_title(self, title):
        max_size = 30
        if len(title) > max_size:
            title = title[:max_size - 3] + "..."
        self.label.set_text(title)

    def set_icon(self, img):
        icon = img.copy()
        icon.thumbnail((24, 24))
        pixbuf = pil_to_pixbuf(icon)
        self.icon_widget.set_from_pixbuf(pixbuf)

    def on_close_button_clicked(self, _):
        self.emit('close-clicked')
