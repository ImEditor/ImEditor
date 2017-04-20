#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from interface.tools import SpinButton


class Dialog(Gtk.Dialog):
    def __init__(self, parent, title):
        Gtk.Dialog.__init__(self, transient_for=parent)
        self.set_title(title)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_size_request(300, -1)
        self.set_border_width(10)

        self.values = list()

    def get_values(self):
        if self.values == []:
            return None
        elif len(self.values) == 1:
            return self.values[0]
        else:
            return self.values


def params_dialog(parent, title, limits):
    dialog = Dialog(parent, title)
    label = Gtk.Label('Entrez une valeur')

    default = (limits[0] + limits[1]) / 2
    h_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, limits[0], limits[1], 20)
    h_scale.set_value(default)
    h_scale.set_hexpand(True)
    h_scale.set_valign(Gtk.Align.START)

    cancel_button = Gtk.Button.new_with_label('Cancel')
    cancel_button.connect('clicked', close_dialog, dialog)

    ok_button = Gtk.Button.new_with_label('Confirm')
    ok_button.connect('clicked', apply_filter, h_scale, dialog)
    ok_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    dialog_box = dialog.get_content_area()
    dialog_box.set_spacing(6)
    dialog_box.pack_start(label, False, False, 0)
    dialog_box.pack_start(h_scale, False, False, 0)

    button_box = Gtk.Box(spacing=6)
    button_box.pack_start(cancel_button, True, True, 0)
    button_box.pack_start(ok_button, True, True, 0)
    dialog_box.pack_start(button_box, False, False, 0)

    dialog.show_all()
    dialog.run()
    dialog.destroy()

    return dialog


def properties_dialog(parent, infos):
    dialog = Dialog(parent, 'Image properties')

    dialog_box = dialog.get_content_area()
    dialog_box.set_spacing(6)

    label = Gtk.Label('<b>Mode:</b> {}'.format(infos['mode']))
    label.set_use_markup(True)
    dialog_box.pack_start(label, False, False, 0)
    label = Gtk.Label('<b>Size:</b> {}'.format(infos['size']))
    label.set_use_markup(True)
    dialog_box.pack_start(label, False, False, 0)
    if 'weight' in infos:
        label = Gtk.Label('<b>Weight:</b> {}'.format(infos['weight']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)
    if 'path' in infos:
        label = Gtk.Label('<b>Path:</b> {}'.format(infos['path']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)
    if 'last_access' in infos:
        label = Gtk.Label('<b>Last access:</b> {}'.format(infos['last_access']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)
    if 'last_change' in infos:
        label = Gtk.Label('<b>Last change:</b> {}'.format(infos['last_change']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def apply_filter(button, h_scale, dialog):
    dialog.values.append(int(h_scale.get_value()))
    dialog.destroy()


def new_image_dialog(parent):
    dialog = Dialog(parent, 'New image')

    spin_width = SpinButton(640, 1, 7680)
    spin_height = SpinButton(360, 1, 4320)

    color_button = Gtk.ColorButton()
    color_button.set_use_alpha(False)

    extension_combo = Gtk.ComboBoxText()
    extension_combo.set_entry_text_column(0)
    extensions = ["PNG", "JPEG", "WEBP", "BMP"]
    for elt in extensions:
        extension_combo.append_text(elt)
    extension_combo.set_active(0)

    cancel_button = Gtk.Button.new_with_label('Cancel')
    cancel_button.connect('clicked', close_dialog, dialog)

    ok_button = Gtk.Button.new_with_label('Confirm')
    ok_button.connect('clicked', ok_callback_new_image, spin_width, spin_height, color_button, extension_combo, dialog)
    ok_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    dialog_box = dialog.get_content_area()
    dialog_box.set_spacing(6)

    grid = Gtk.Grid(row_spacing=12, column_spacing=12, column_homogeneous=True)
    grid.attach(Gtk.Label('Width'), 0, 0, 1, 1)
    grid.attach(spin_width, 1, 0, 1, 1)
    grid.attach(Gtk.Label('Height'), 2, 0, 1, 1)
    grid.attach(spin_height, 3, 0, 1, 1)

    grid.attach(Gtk.Label('Background color'), 0, 1, 1, 1)
    grid.attach(color_button, 1, 1, 3, 1)
    grid.attach(Gtk.Label('Format'), 0, 2, 1, 1)
    grid.attach(extension_combo, 1, 2, 3, 1)

    grid.attach(cancel_button, 0, 3, 2, 1)
    grid.attach(ok_button, 2, 3, 2, 1)

    dialog_box.add(grid)

    dialog.show_all()
    dialog.run()
    dialog.destroy()
    return dialog


def close_dialog(button, dialog):
    dialog.destroy()


def ok_callback_new_image(button, spin_width, spin_height, color_button, extension_combo, dialog):
    width = spin_width.get_value_as_int()
    height = spin_height.get_value_as_int()
    size = (width, height)
    color = color_button.get_rgba().to_string()
    extension = extension_combo.get_active_text()
    dialog.values.append(size)
    dialog.values.append(color)
    dialog.values.append(extension)
    dialog.destroy()


def file_dialog(parent, action, filename=None):
    if action == 'open':
        dialog = Gtk.FileChooserDialog('Choose a file',
            parent,
            Gtk.FileChooserAction.OPEN,
            ('Cancel', Gtk.ResponseType.CANCEL,
            'Open', Gtk.ResponseType.OK))
    elif action == 'save':
        dialog = Gtk.FileChooserDialog('Choose a file',
            parent,
            Gtk.FileChooserAction.SAVE,
            ('Cancel', Gtk.ResponseType.CANCEL,
            'Confirm', Gtk.ResponseType.OK))
        dialog.set_current_name(filename)
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        filename = dialog.get_filename()
    else:
        filename = None
    dialog.destroy()
    return filename
