#!/usr/bin/python3

from gi.repository import Gtk

def dialog(func, parent, title, limits):
    # Adjustment: value, lower, upper, step increment, page increment, page size
    # Tags: MODAL: can't click on main window

    dialog_window = Gtk.Dialog(parent)
    dialog_window.set_title(title)
    dialog_window.set_modal(True)

    dialog_window.set_resizable(False)
    dialog_window.set_size_request(300, -1)
    dialog_window.set_border_width(10)
    dialog_box = dialog_window.get_content_area()

    label = Gtk.Label('Entrez une valeur')

    default = (limits[0] + limits[1]) / 2
    adjustment = Gtk.Adjustment(default, limits[0], limits[1], 20, 10, 0)
    h_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
    h_scale.set_digits(0)
    h_scale.set_hexpand(True)
    h_scale.set_valign(Gtk.Align.START)

    cancel_button = Gtk.Button.new_with_label("Annuler")
    cancel_button.connect("clicked", lambda arg: cancel(dialog_window))

    ok_button = Gtk.Button.new_with_label("Ok")
    ok_button.connect("clicked", lambda arg: apply(h_scale, func, parent, dialog_window))

    dialog_box.pack_start(label, False, False, 0)
    dialog_box.pack_start(h_scale, False, False, 0)
    dialog_box.pack_start(cancel_button, False, False, 0)
    dialog_box.pack_start(ok_button, False, False, 0)

    dialog_window.show_all()
    dialog_window.run()

def cancel(dialog):
    dialog.destroy()

def apply(h_scale, func, parent, dialog_window):
    value = int(h_scale.get_value())
    parent.filter(func, value)
    dialog_window.destroy()

# http://python-gtk-3-tutorial.readthedocs.org/en/latest/dialogs.html
# https://developer.gnome.org/gtk3/stable/GtkDialog.html
