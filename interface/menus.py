#!/usr/bin/python3

from gi.repository import Gtk, Gdk, GdkPixbuf

from filters import base

def create_menus(self):
    # Menu:
    action_group = Gtk.ActionGroup(name='menu')

    # File:
    action_filemenu = Gtk.Action(name="FileMenu", label="Fichier")
    action_group.add_action(action_filemenu)

    action_fileopen = Gtk.Action(name='FileOpen', stock_id=Gtk.STOCK_OPEN)
    action_fileopen.connect('activate', self.open_file)
    action_group.add_action_with_accel(action_fileopen, '<control>O')

    action_filesave = Gtk.Action(name='FileSave', stock_id=Gtk.STOCK_SAVE)
    action_filesave.connect('activate', self.file_save)
    action_group.add_action_with_accel(action_filesave, '<control>S')

    action_filequit = Gtk.Action(name='FileQuit', stock_id=Gtk.STOCK_QUIT)
    action_filequit.connect('activate', self.quit_app)
    action_group.add_action_with_accel(action_filequit, '<control>Q')

    # Edit:
    action_editmenu = Gtk.Action(name="EditMenu", label="Édition")
    action_group.add_action(action_editmenu)

    action_editundo = Gtk.Action(name='EditUndo', stock_id=Gtk.STOCK_UNDO)
    #action_editundo.connect('activate', self.undo)
    action_group.add_action_with_accel(action_editundo, '<control>Z')

    action_editredo = Gtk.Action(name='EditRedo', stock_id=Gtk.STOCK_REDO)
    #action_editredo.connect('activate', self.paste)
    action_group.add_action_with_accel(action_editredo, '<control>Y')

    action_editcopy = Gtk.Action(name='EditCopy', stock_id=Gtk.STOCK_COPY)
    #action_editcopy.connect('activate', self.copy)
    action_group.add_action_with_accel(action_editcopy, '<control>C')

    action_editpaste = Gtk.Action(name='EditPaste', stock_id=Gtk.STOCK_PASTE)
    #action_editpaste.connect('activate', self.paste)
    action_group.add_action_with_accel(action_editpaste, '<control>V')

    action_editcut = Gtk.Action(name='EditCut', stock_id=Gtk.STOCK_CUT)
    #action_editcut.connect('activate', self.paste)
    action_group.add_action_with_accel(action_editcut, '<control>C')

    action_rotateleft = Gtk.Action(name='RotateLeft', label='Rotation -90°')
    action_rotateleft.connect('activate', lambda arg: self.filter(base.rotate_left))
    action_group.add_action(action_rotateleft)

    action_rotateright = Gtk.Action(name='RotateRight', label='Rotation 90°')
    action_rotateright.connect('activate', lambda arg: self.filter(base.rotate_right))
    action_group.add_action(action_rotateright)

    # Base filters:
    action_basefilters = Gtk.Action(name="FiltersMenu", label="Filters")
    action_group.add_action(action_basefilters)

    action_basenegative = Gtk.Action(name='BaseNegative', label='Négatif')
    action_basenegative.connect('activate', lambda arg: self.filter(base.negative))
    action_group.add_action(action_basenegative)

    action_basebw = Gtk.Action(name='BaseBW', label='Noir et blanc')
    action_basebw.connect('activate', lambda arg: self.filter(base.black_white))
    action_group.add_action(action_basebw)

    # UI:
    uimanager = Gtk.UIManager()
    uimanager.add_ui_from_file('interface/interface.ui')
    self.add_accel_group(uimanager.get_accel_group())
    uimanager.insert_action_group(action_group)

    return uimanager.get_widget("/MenuBar"), uimanager.get_widget("/Toolbar")
