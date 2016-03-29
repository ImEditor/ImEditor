#!/usr/bin/python3

from gi.repository import Gtk

class MyDialog(Gtk.Dialog):
    def __init__(self, parent, title):
        Gtk.Dialog.__init__(self, parent)
        self.set_title(title)
        self.set_modal(True)

        self.set_resizable(False)
        self.set_size_request(300, -1)
        self.set_border_width(10)

def dialog_param(func, parent, title, limits):
    # Adjustment: value, lower, upper, step increment, page increment, page size
    # Tags: MODAL: can't click on main window
    dialog = MyDialog(parent, title)
    label = Gtk.Label('Entrez une valeur')

    default = (limits[0] + limits[1]) / 2
    adjustment = Gtk.Adjustment(default, limits[0], limits[1], 20, 10, 0)
    h_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
    h_scale.set_digits(0)
    h_scale.set_hexpand(True)
    h_scale.set_valign(Gtk.Align.START)

    cancel_button = Gtk.Button.new_with_label("Annuler")
    cancel_button.connect("clicked", lambda arg: close(dialog))

    ok_button = Gtk.Button.new_with_label("Ok")
    ok_button.connect("clicked", lambda arg: apply(parent, h_scale, func, dialog))

    dialog_box = dialog.get_content_area()
    dialog_box.pack_start(label, False, False, 0)
    dialog_box.pack_start(h_scale, False, False, 0)
    dialog_box.pack_start(cancel_button, False, False, 0)
    dialog_box.pack_start(ok_button, False, False, 0)
    dialog.show_all()
    dialog.run()

def dialog_new_image(parent):
    dialog = MyDialog(parent, 'Nouvelle image')

    label_width = Gtk.Label('Largeur')
    adj_width = Gtk.Adjustment(640, 1, 2048, 40, 20, 0)
    spin_width = Gtk.SpinButton()
    spin_width.set_adjustment(adj_width)

    label_height = Gtk.Label('Hauteur')
    adj_height = Gtk.Adjustment(360, 1, 1080, 40, 20, 0)
    spin_height = Gtk.SpinButton()
    spin_height.set_adjustment(adj_height)

    color_chooser = Gtk.ColorChooserWidget()

    cancel_button = Gtk.Button.new_with_label("Annuler")
    cancel_button.connect("clicked", lambda arg: close(dialog))

    ok_button = Gtk.Button.new_with_label("Ok")
    ok_button.connect("clicked", lambda arg: new_image(parent, spin_width, spin_height, color_chooser, dialog))

    dialog_box = dialog.get_content_area()
    dialog_box.pack_start(spin_width, False, False, 0)
    dialog_box.pack_start(spin_height, False, False, 0)
    dialog_box.pack_start(color_chooser, False, False, 0)
    dialog_box.pack_start(cancel_button, False, False, 0)
    dialog_box.pack_start(ok_button, False, False, 0)
    dialog.show_all()
    dialog.run()

def close(dialog):
    dialog.destroy()

def apply(parent, h_scale, func, dialog):
    value = int(h_scale.get_value())
    parent.filter(func, value)
    dialog.destroy()
    close(dialog)

def new_image(parent, spin_width, spin_height, color_chooser, dialog):
    width = spin_width.get_value_as_int()
    height = spin_height.get_value_as_int()
    color = color_chooser.get_rgba().to_string()
    parent.new_image((width, height), color)
    close(dialog)
