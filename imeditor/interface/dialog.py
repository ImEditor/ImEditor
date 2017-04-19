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

    cancel_button = Gtk.Button.new_with_label("Annuler")
    cancel_button.connect("clicked", close_dialog, dialog)

    ok_button = Gtk.Button.new_with_label("Valider")
    ok_button.connect("clicked", apply_filter, h_scale, dialog)

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
    dialog = Dialog(parent, 'Propriétés de l\'image')

    dialog_box = dialog.get_content_area()
    dialog_box.set_spacing(6)

    label = Gtk.Label('<b>Mode :</b> {}'.format(infos['mode']))
    label.set_use_markup(True)
    dialog_box.pack_start(label, False, False, 0)
    label = Gtk.Label('<b>Taille :</b> {}'.format(infos['size']))
    label.set_use_markup(True)
    dialog_box.pack_start(label, False, False, 0)
    if 'weight' in infos:
        label = Gtk.Label('<b>Poids :</b> {}'.format(infos['weight']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)
    if 'path' in infos:
        label = Gtk.Label('<b>Chemin :</b> {}'.format(infos['path']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)
    if 'last_access' in infos:
        label = Gtk.Label('<b>Dernier accès :</b> {}'.format(infos['last_access']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)
    if 'last_change' in infos:
        label = Gtk.Label('<b>Dernière modification :</b> {}'.format(infos['last_change']))
        label.set_use_markup(True)
        dialog_box.pack_start(label, False, False, 0)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def apply_filter(button, h_scale, dialog):
    dialog.values.append(int(h_scale.get_value()))
    dialog.destroy()


def new_image_dialog(parent):
    dialog = Dialog(parent, 'Nouvelle image')

    spin_width = SpinButton(640, 1, 7680)
    spin_height = SpinButton(360, 1, 4320)

    color_chooser = Gtk.ColorChooserWidget()
    color_chooser.set_use_alpha(False)

    cancel_button = Gtk.Button.new_with_label("Annuler")
    cancel_button.connect("clicked", close_dialog, dialog)

    ok_button = Gtk.Button.new_with_label("Valider")
    ok_button.connect("clicked", ok_callback_new_image, spin_width, spin_height, color_chooser, dialog)

    dialog_box = dialog.get_content_area()
    dialog_box.set_spacing(6)

    spins_box = Gtk.Box(spacing=6)
    spins_box.pack_start(Gtk.Label('Largeur :'), True, True, 0)
    spins_box.pack_start(spin_width, True, True, 0)
    spins_box.pack_start(Gtk.Label('Hauteur :'), True, True, 0)
    spins_box.pack_start(spin_height, True, True, 0)
    button_box = Gtk.Box(spacing=6)
    button_box.pack_start(cancel_button, True, True, 0)
    button_box.pack_start(ok_button, True, True, 0)

    dialog_box.pack_start(spins_box, False, False, 0)
    dialog_box.pack_start(color_chooser, False, False, 0)
    dialog_box.pack_start(button_box, False, False, 0)
    dialog.show_all()
    dialog.run()
    dialog.destroy()

    return dialog


def close_dialog(button, dialog):
    dialog.destroy()


def ok_callback_new_image(button, spin_width, spin_height, color_chooser, dialog):
    width = spin_width.get_value_as_int()
    height = spin_height.get_value_as_int()
    size = (width, height)
    color = color_chooser.get_rgba().to_string()
    dialog.values.append(size)
    dialog.values.append(color)
    dialog.destroy()


def file_dialog(parent, action):
    if action == 'open':
        dialog = Gtk.FileChooserDialog('Choisissez un fichier',
            parent,
            Gtk.FileChooserAction.OPEN,
            ("Annuler", Gtk.ResponseType.CANCEL,
            "Ouvrir", Gtk.ResponseType.OK))
    elif action == 'save':
        dialog = Gtk.FileChooserDialog('Choisissez un fichier',
            parent,
            Gtk.FileChooserAction.SAVE,
            ("Annuler", Gtk.ResponseType.CANCEL,
            "Ok", Gtk.ResponseType.OK))
        dialog.set_current_name('untitled.png')
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        filename = dialog.get_filename()
    else:
        filename = None
    dialog.destroy()
    return filename
