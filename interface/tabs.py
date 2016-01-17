#!/usr/bin/python3

from gi.repository import Gtk, GObject

class TabLabel(Gtk.Box):
    """Define the label on the tab."""
    __gsignals__ = {
        'close-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }
    def __init__(self, title):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(5)

        # icon

        # Label:
        label = Gtk.Label(title)
        self.pack_start(label, True, True, 0)

        # Close button:
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.set_focus_on_click(False)
        button.add(Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU))
        button.connect('clicked', self.button_clicked)
        self.pack_start(button, False, False, 0)

        self.show_all()

    def button_clicked(self, _):
        self.emit('close-clicked')
