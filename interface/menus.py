#!/usr/bin/python3

from gi.repository import Gtk, Gdk, GdkPixbuf

from filters import base

def create_menus(self):
    # Menu:
    action_group = Gtk.ActionGroup(name='menu')

    # File:
    action_filemenu = Gtk.Action(name="FileMenu", label="Fichier")
    action_group.add_action(action_filemenu)

    action_fileopen = Gtk.Action(name='FileOpen', label='Ouvrir')
    action_fileopen.connect('activate', self.open_image)
    action_fileopen.set_icon_name('document-open')
    action_group.add_action_with_accel(action_fileopen, '<control>O')

    action_filesave = Gtk.Action(name='FileSave', label='Enregistrer')
    action_filesave.connect('activate', self.file_save)
    action_filesave.set_icon_name('document-save')
    action_group.add_action_with_accel(action_filesave, '<control>S')

    action_filesaveas = Gtk.Action(name='FileSaveAs', label='Enregistrer sous')
    action_filesaveas.connect('activate', self.file_save_as)
    action_filesaveas.set_icon_name('document-save-as')
    action_group.add_action_with_accel(action_filesaveas, '<shift><control>S')

    action_filequit = Gtk.Action(name='FileQuit', label='Quitter')
    action_filequit.connect('activate', self.quit_app)
    action_group.add_action_with_accel(action_filequit, '<control>Q')

    # Edit:
    action_editmenu = Gtk.Action(name="EditMenu", label="Édition")
    action_group.add_action(action_editmenu)

    action_editundo = Gtk.Action(name='EditUndo', label='Annuler')
    action_editundo.connect('activate', lambda arg: self.history(-1))
    action_editundo.set_icon_name('edit-undo')
    action_group.add_action_with_accel(action_editundo, '<control>Z')

    action_editredo = Gtk.Action(name='EditRedo', label='Rétablir')
    action_editredo.connect('activate', lambda arg: self.history(1))
    action_editredo.set_icon_name('edit-redo')
    action_group.add_action_with_accel(action_editredo, '<control>Y')

    action_editcopy = Gtk.Action(name='EditCopy', label='Copier')
    #action_editcopy.connect('activate', self.copy)
    action_editcopy.set_icon_name('edit-copy')
    action_group.add_action_with_accel(action_editcopy, '<control>C')

    action_editpaste = Gtk.Action(name='EditPaste', label='Coller')
    #action_editpaste.connect('activate', self.paste)
    action_editpaste.set_icon_name('edit-paste')
    action_group.add_action_with_accel(action_editpaste, '<control>V')

    action_editcut = Gtk.Action(name='EditCut', label='Couper')
    #action_editcut.connect('activate', self.paste)
    action_editcut.set_icon_name('edit-cut')
    action_group.add_action_with_accel(action_editcut, '<control>C')

    action_rotateleft = Gtk.Action(name='RotateLeft', label='Rotation -90°')
    action_rotateleft.connect('activate', lambda arg: self.filter(base.rotate_left))
    action_rotateleft.set_icon_name('object-rotate-left')
    action_group.add_action(action_rotateleft)

    action_rotateright = Gtk.Action(name='RotateRight', label='Rotation 90°')
    action_rotateright.connect('activate', lambda arg: self.filter(base.rotate_right))
    action_rotateright.set_icon_name('object-rotate-right')
    action_group.add_action(action_rotateright)

    # Base filters:
    action_basefilters = Gtk.Action(name="FiltersMenu", label="Filtres")
    action_group.add_action(action_basefilters)

    action_basenegative = Gtk.Action(name='BaseNegative', label='Négatif')
    action_basenegative.connect('activate', lambda arg: self.filter(base.negative))
    action_group.add_action(action_basenegative)

    action_basebw = Gtk.Action(name='BaseBW', label='Noir et blanc')
    action_basebw.connect('activate', lambda arg: self.filter(base.black_white))
    action_group.add_action(action_basebw)

    action_basered = Gtk.Action(name='BaseRed', label='Rouge')
    action_basered.connect('activate', lambda arg: self.filter(base.red))
    action_group.add_action(action_basered)

    action_basegreen = Gtk.Action(name='BaseGreen', label='Vert')
    action_basegreen.connect('activate', lambda arg: self.filter(base.green))
    action_group.add_action(action_basegreen)

    action_baseblue = Gtk.Action(name='BaseBlue', label='Bleu')
    action_baseblue.connect('activate', lambda arg: self.filter(base.blue))
    action_group.add_action(action_baseblue)

    action_baseGL = Gtk.Action(name='BaseGL', label='Niveau de gris')
    action_baseGL.connect('activate', lambda arg: self.filter(base.gray_level))
    action_group.add_action(action_baseGL)

    action_baselighten = Gtk.Action(name='BaseLighten', label='Éclaircir')
    action_baselighten.connect('activate', lambda arg: self.filter(base.lighten))
    action_group.add_action(action_baselighten)

    action_basedarken = Gtk.Action(name='BaseDarken', label='Assombrir')
    action_basedarken.connect('activate', lambda arg: self.filter(base.darken))
    action_group.add_action(action_basedarken)

    # Help:
    action_help = Gtk.Action(name="HelpMenu", label="Aide")
    action_group.add_action(action_help)

    action_helpabout = Gtk.Action(name='HelpAbout', label='À propos')
    action_helpabout.connect('activate', self.about)
    action_group.add_action(action_helpabout)

    # UI:
    uimanager = Gtk.UIManager()
    uimanager.add_ui_from_file('interface/interface.ui')
    self.add_accel_group(uimanager.get_accel_group())
    uimanager.insert_action_group(action_group)

    return uimanager.get_widget("/MenuBar"), uimanager.get_widget("/Toolbar")
