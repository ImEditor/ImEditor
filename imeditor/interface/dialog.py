#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

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

        self.dialog_box = self.get_content_area()
        self.dialog_box.set_spacing(6)

    def get_values(self):
        if self.values == []:
            return None
        elif len(self.values) == 1:
            return self.values[0]
        else:
            return self.values

    def launch(self):
        self.show_all()
        self.run()
        self.destroy()


def params_dialog(parent, title, limits):
    def callback_apply_filter(button, h_scale, dialog):
        dialog.values.append(int(h_scale.get_value()))
        dialog.destroy()

    dialog = Dialog(parent, title)

    default = (limits[0] + limits[1]) / 2
    h_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, limits[0], limits[1], 20)
    h_scale.set_value(default)
    h_scale.set_hexpand(True)
    h_scale.set_valign(Gtk.Align.START)

    ok_button = Gtk.Button.new_with_label('Apply')
    ok_button.connect('clicked', callback_apply_filter, h_scale, dialog)
    ok_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    dialog.dialog_box.pack_start(h_scale, False, False, 0)

    button_box = Gtk.Box(spacing=6)
    button_box.pack_start(ok_button, True, True, 0)

    dialog.dialog_box.pack_start(button_box, False, False, 0)
    dialog.launch()
    return dialog


def details_dialog(parent, infos):
    dialog = Dialog(parent, 'Image details')

    grid = Gtk.Grid(row_spacing=12, column_spacing=12, column_homogeneous=True)
    grid.attach(Gtk.Label('<b>Mode</b>', use_markup=True), 0, 0, 1, 1)
    grid.attach(Gtk.Label(infos['mode']), 1, 0, 1, 1)
    grid.attach(Gtk.Label('<b>Size</b>', use_markup=True), 0, 1, 1, 1)
    grid.attach(Gtk.Label(infos['size']), 1, 1, 1, 1)

    if len(infos) > 2:
        grid.attach(Gtk.Label('<b>Weight</b>', use_markup=True), 0, 2, 1, 1)
        grid.attach(Gtk.Label(infos['weight']), 1, 2, 1, 1)
        grid.attach(Gtk.Label('<b>Path</b>', use_markup=True), 0, 3, 1, 1)
        grid.attach(Gtk.Label(infos['path']), 1, 3, 1, 1)
        grid.attach(Gtk.Label('<b>Last access</b>', use_markup=True), 0, 4, 1, 1)
        grid.attach(Gtk.Label(infos['last_access']), 1, 4, 1, 1)
        grid.attach(Gtk.Label('<b>Last change</b>', use_markup=True), 0, 5, 1, 1)
        grid.attach(Gtk.Label(infos['last_change']), 1, 5, 1, 1)

    dialog.dialog_box.add(grid)
    dialog.launch()


def new_image_dialog(parent):
    def on_template_changed(button):
        template = button.get_active_text()
        templates = {
            'Favicon': (16, 16),
            'A3': (3508, 4960),
            'A4': (3508, 2480),
            'A5': (2480, 1748),
            'A6': (1748, 1240)
        }
        spin_width.set_value(templates[template][0])
        spin_height.set_value(templates[template][1])

    def on_transparent_toggled(button):
        color_button.set_sensitive(not color_button.get_sensitive())

    def callback_new_image(button, name_entry, spin_width, spin_height, color_button, extension_combo, transparent_check, dialog):
        name = name_entry.get_text()
        width = spin_width.get_value_as_int()
        height = spin_height.get_value_as_int()
        size = (width, height)
        color = color_button.get_rgba().to_string()
        extension = extension_combo.get_active_text()
        transparent = transparent_check.get_active()
        dialog.values += [name, size, color, extension, transparent]
        dialog.destroy()

    dialog = Dialog(parent, 'New image')

    name_entry = Gtk.Entry()
    name_entry.set_text('untitled')

    template_combo = Gtk.ComboBoxText()
    template_combo.connect('changed', on_template_changed)
    template_combo.set_entry_text_column(0)
    templates = ['Favicon', 'A3', 'A4', 'A5', 'A6']
    for elt in templates:
        template_combo.append_text(elt)
    spin_width = SpinButton(640, 1, 10000)
    spin_height = SpinButton(360, 1, 10000)

    color_button = Gtk.ColorButton()
    color_button.set_use_alpha(False)
    color_button.set_rgba(Gdk.RGBA(1, 1, 1, 1))

    extension_combo = Gtk.ComboBoxText()
    extension_combo.set_entry_text_column(0)
    extensions = ['PNG', 'JPEG', 'WEBP', 'BMP', 'ICO']
    for elt in extensions:
        extension_combo.append_text(elt)
    extension_combo.set_active(0)

    transparent_check = Gtk.CheckButton()
    transparent_check.connect('toggled', on_transparent_toggled)

    ok_button = Gtk.Button.new_with_label('Create')
    ok_button.connect('clicked', callback_new_image, name_entry, spin_width, spin_height, color_button, extension_combo, transparent_check, dialog)
    ok_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    grid = Gtk.Grid(row_spacing=12, column_spacing=12)
    grid.attach(Gtk.Label('Name', xalign=0.0), 0, 0, 2, 1)
    grid.attach(name_entry, 2, 0, 2, 1)
    grid.attach(Gtk.Label('Template', xalign=0.0), 0, 1, 2, 1)
    grid.attach(template_combo, 2, 1, 2, 1)
    grid.attach(Gtk.Label('Width', xalign=0.0), 0, 2, 1, 1)
    grid.attach(spin_width, 1, 2, 1, 1)
    grid.attach(Gtk.Label('Height', xalign=0.0), 2, 2, 1, 1)
    grid.attach(spin_height, 3, 2, 1, 1)
    grid.attach(Gtk.Label('Background color', xalign=0.0), 0, 3, 2, 1)
    grid.attach(color_button, 2, 3, 2, 1)
    grid.attach(Gtk.Label('Transparent', xalign=0.0), 0, 4, 2, 1)
    grid.attach(transparent_check, 2, 4, 2, 1)
    grid.attach(Gtk.Label('Format', xalign=0.0), 0, 5, 2, 1)
    grid.attach(extension_combo, 2, 5, 2, 1)
    grid.attach(ok_button, 0, 6, 4, 1)

    dialog.dialog_box.add(grid)
    dialog.set_focus(ok_button)
    dialog.launch()
    return dialog


def file_dialog(parent, action, filename=None):
    if action == 'open':
        dialog = Gtk.FileChooserDialog('Open image',
            parent,
            Gtk.FileChooserAction.OPEN,
            ('Cancel', Gtk.ResponseType.CANCEL,
            'Open', Gtk.ResponseType.OK))
    elif action == 'save':
        dialog = Gtk.FileChooserDialog('Save image',
            parent,
            Gtk.FileChooserAction.SAVE,
            ('Cancel', Gtk.ResponseType.CANCEL,
            'Save', Gtk.ResponseType.OK))
        dialog.set_current_name(filename)
    response = dialog.run()
    filename = dialog.get_filename() if response == Gtk.ResponseType.OK else None
    dialog.destroy()
    return filename
