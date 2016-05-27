# -*- coding: utf-8 -*-
#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

def create_menubar(parent, actions):
    editor = parent.editor
    all_actions = list()
    for key in actions:
        all_actions.extend(actions[key])

    for action in all_actions:
        name = action['name']
        callback = action['callback']
        act = Gio.SimpleAction.new(name, None)
        if 'params' in action.keys():
            params = action['params']
            act.connect('activate', eval(callback), params)
        else:
            act.connect('activate', eval(callback))
        parent.add_action(act)

def create_toolbar(parent):
    toolbar = Gtk.Toolbar()

    new_button = Gtk.ToolButton.new()
    new_button.set_icon_name('document-new')
    toolbar.insert(new_button, 0)
    new_button.show()
    new_button.set_action_name('win.new')

    open_button = Gtk.ToolButton.new()
    open_button.set_icon_name('document-open')
    toolbar.insert(open_button, 1)
    open_button.show()
    open_button.set_action_name('win.open')

    save_button = Gtk.ToolButton.new()
    save_button.set_icon_name('document-save')
    toolbar.insert(save_button, 2)
    save_button.show()
    save_button.set_action_name('win.save')

    save_as_button = Gtk.ToolButton.new()
    save_as_button.set_icon_name('document-save-as')
    toolbar.insert(save_as_button, 3)
    save_as_button.show()
    save_as_button.set_action_name('win.save_as')

    undo_button = Gtk.ToolButton.new()
    undo_button.set_icon_name('edit-undo')
    toolbar.insert(undo_button, 4)
    undo_button.show()
    undo_button.set_action_name('win.undo')

    redo_button = Gtk.ToolButton.new()
    redo_button.set_icon_name('edit-redo')
    toolbar.insert(redo_button, 5)
    redo_button.show()
    redo_button.set_action_name('win.redo')

    rotate_left_button = Gtk.ToolButton.new()
    rotate_left_button.set_icon_name('object-rotate-left')
    toolbar.insert(rotate_left_button, 6)
    rotate_left_button.show()
    rotate_left_button.set_action_name('win.rotate_left')

    rotate_right_button = Gtk.ToolButton.new()
    rotate_right_button.set_icon_name('object-rotate-right')
    toolbar.insert(rotate_right_button, 7)
    rotate_right_button.show()
    rotate_right_button.set_action_name('win.rotate_right')

    select_button = Gtk.ToolButton.new()
    pixbuf = Gdk.Cursor(Gdk.CursorType.ARROW).get_image()
    select_button.set_icon_widget(Gtk.Image.new_from_pixbuf(pixbuf))
    toolbar.insert(select_button, 8)
    select_button.show()
    select_button.set_action_name('win.select')

    draw_button = Gtk.ToolButton.new()
    draw_button.set_icon_name('applications-graphics')
    toolbar.insert(draw_button, 9)
    draw_button.show()
    draw_button.set_action_name('win.draw-brush')

    parent.fullscreen_button = Gtk.ToolButton.new()
    parent.fullscreen_button.set_icon_name('view-fullscreen')
    toolbar.insert(parent.fullscreen_button, 10)
    parent.fullscreen_button.set_action_name('win.fullscreen')

    toolbar.set_hexpand(True) # with extra horizontal space
    toolbar.show()
    return toolbar
