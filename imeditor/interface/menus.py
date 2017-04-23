#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


def create_menubar(parent, actions):
    all_actions = list()
    for key in actions:
        all_actions.extend(actions[key])

    for action in all_actions:
        name = action['name']
        callback = action['callback']
        act = Gio.SimpleAction.new(name, None)
        if 'params' in action.keys():
            params = action['params']
            act.connect('activate', getattr(parent, callback), params)
        else:
            act.connect('activate', getattr(parent, callback))
        parent.add_action(act)


def create_toolbar(parent):
    toolbar = Gtk.Toolbar()
    toolbar.set_hexpand(True)

    new_button = Gtk.ToolButton.new()
    new_button.set_icon_name('document-new')
    toolbar.insert(new_button, 0)
    new_button.set_action_name('win.new')

    open_button = Gtk.ToolButton.new()
    open_button.set_icon_name('document-open')
    toolbar.insert(open_button, 1)
    open_button.set_action_name('win.open')

    save_button = Gtk.ToolButton.new()
    save_button.set_icon_name('document-save')
    toolbar.insert(save_button, 2)
    save_button.set_action_name('win.save')

    save_as_button = Gtk.ToolButton.new()
    save_as_button.set_icon_name('document-save-as')
    toolbar.insert(save_as_button, 3)
    save_as_button.set_action_name('win.save_as')

    undo_button = Gtk.ToolButton.new()
    undo_button.set_icon_name('edit-undo')
    toolbar.insert(undo_button, 4)
    undo_button.set_action_name('win.undo')

    redo_button = Gtk.ToolButton.new()
    redo_button.set_icon_name('edit-redo')
    toolbar.insert(redo_button, 5)
    redo_button.set_action_name('win.redo')

    rotate_left_button = Gtk.ToolButton.new()
    rotate_left_button.set_icon_name('object-rotate-left')
    toolbar.insert(rotate_left_button, 6)
    rotate_left_button.set_action_name('win.rotate_left')

    rotate_right_button = Gtk.ToolButton.new()
    rotate_right_button.set_icon_name('object-rotate-right')
    toolbar.insert(rotate_right_button, 7)
    rotate_right_button.set_action_name('win.rotate_right')

    select_button = Gtk.ToolButton.new()
    select_button.set_icon_widget(Gtk.Image.new_from_file('assets/select.png'))
    toolbar.insert(select_button, 8)
    select_button.set_action_name('win.select')

    pencil_button = Gtk.ToolButton.new()
    pencil_button.set_icon_widget(Gtk.Image.new_from_file('assets/pencil.png'))
    toolbar.insert(pencil_button, 9)
    pencil_button.set_action_name('win.pencil')

    parent.fullscreen_button = Gtk.ToolButton.new()
    parent.fullscreen_button.set_icon_name('view-fullscreen')
    toolbar.insert(parent.fullscreen_button, 10)
    parent.fullscreen_button.set_action_name('win.fullscreen')

    return toolbar
