#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk

from editor.editor import Editor
from interface.tools import pil_to_pixbuf


class Tab(Gtk.ScrolledWindow):
    def __init__(self, win, img, title, filename):
        Gtk.ScrolledWindow.__init__(self)
        self.win = win
        self.editor = Editor(self.win, self, img, filename)

        pixbuf = pil_to_pixbuf(img)
        self.img_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        event_box = Gtk.EventBox()
        event_box.set_events(Gdk.EventMask.BUTTON1_MOTION_MASK)
        event_box.connect('button-press-event', self.editor.press_task)
        event_box.connect('motion-notify-event', self.editor.move_task)
        event_box.connect('button-release-event', self.editor.release_task)
        frame = Gtk.Frame(hexpand=True, vexpand=True)
        frame.set_halign(Gtk.Align.CENTER)
        frame.set_valign(Gtk.Align.CENTER)
        frame.set_name('TabFrame')
        style_provider = Gtk.CssProvider()
        css = b"""
        #TabFrame {
            background: url('assets/transparent.png');
        }
        """
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        event_box.add(self.img_widget)
        frame.add(event_box)
        self.add(frame)

        self.tab_label = TabLabel(title, img)
        self.tab_label.connect('close-clicked', self.on_close_button_clicked)

        self.show_all()

    def update_image(self, new_img):
        self.tab_label.set_icon(new_img)
        pixbuf = pil_to_pixbuf(new_img)
        self.img_widget.set_from_pixbuf(pixbuf)

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
