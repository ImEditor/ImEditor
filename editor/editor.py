#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from interface import dialog
from filters import base

def img_open(func):
    def inner(self, *args, **kwargs):
        if len(self.images) > 0:
            return func(self, *args, **kwargs)
    return inner

class Editor(object):
    def __init__(self):
        super(Editor, self).__init__()
        self.images = list()
        self.MAX_HIST = 10

    def set_win(self, win):
        self.win = win

    @img_open
    def close_image(self, index):
        for img in self.images[index][0]:
            img.close()
        self.images = self.images[:index] + self.images[index+1:]

    def add_image(self, img, filename, index):
        self.images.append([[img], filename, index])

    @img_open
    def apply_filter(self, action, parameter, func, value=None):
        func = eval(func)
        page_num = self.win.notebook.get_current_page()
        index_img = self.images[page_num][2]
        if value is None:
            new_img = func(self.images[page_num][0][index_img])
        else:
            new_img = func(self.images[page_num][0][index_img], value)
        self.win.update_image(new_img, page_num)
        self.images[page_num][0] = self.images[page_num][0][:index_img+1]
        self.images[page_num][0].append(new_img)
        self.images[page_num][2] += 1
        if len(self.images[page_num][0]) > self.MAX_HIST:
            self.images[page_num][0].pop(0)
            self.images[page_num][2] -= 1

    @img_open
    def filter_with_params(self, action, parameter, params):
        func = params[0]
        title = params[1]
        limits = params[2]
        params_dialog = dialog.params_dialog(func, self.win, title, limits)
        value = params_dialog.get_values()
        if value is not None:
            self.apply_filter(None, None, func, value)

    @img_open
    def history(self, action, parameter, num):
        page_num = self.win.notebook.get_current_page()
        if len(self.images[page_num][0]) >= 2:
            index_img = self.images[page_num][2]
            if num == -1: # Undo:
                if index_img >= 1:
                    self.images[page_num][2] += num
                    index_img = self.images[page_num][2]
                    self.win.update_image(self.images[page_num][0][index_img], page_num)
            else: # Redo:
                if index_img + 1 < len(self.images[page_num][0]):
                    self.images[page_num][2] += num
                    index_img = self.images[page_num][2]
                    self.win.update_image(self.images[page_num][0][index_img], page_num)

    @img_open
    def file_save(self, action, parameter):
        page_num = self.win.notebook.get_current_page()
        index_img = self.images[page_num][2]
        self.images[page_num][0][index_img].save(self.images[page_num][1])

    @img_open
    def file_save_as(self, action, parameter):
        page_num = self.win.notebook.get_current_page()

        dialog = Gtk.FileChooserDialog('Choisissez un fichier', self.win,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            index_img = self.images[page_num][2]
            self.images[page_num][0][index_img].save(filename)
            self.win.close_tab(page_num)
            self.win.create_tab(filename)
        dialog.destroy()

    @img_open
    def properties(self, action, parameter):
        page_num = self.win.notebook.get_current_page()
        index_img = self.images[page_num][2]
        img = self.images[page_num][0][index_img]
        dialog = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, 'Propriétés de l\'image')
        message = '<b>Taille : </b>' + str(img.width) + 'x' + str(img.height) + ' <b>Mode : </b>' + img.mode
        dialog.format_secondary_markup(message)
        dialog.run()
        dialog.destroy()
