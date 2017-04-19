#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import Image
from os import path

from interface import dialog
from filters import base
from editor.image import ImageObject
from editor.tools import get_middle_mouse, get_infos
from editor.draw import draw_point, draw_shape


def img_open(func):
    def inner(self, *args, **kwargs):
        if len(self.images) > 0:
            return func(self, *args, **kwargs)
    return inner


class Editor(object):
    def __init__(self, parent):
        super(Editor, self).__init__()
        self.parent = parent

        self.images = list()
        self.MAX_HIST = 10

        self.task = 0  # 0 -> select, 1 -> paste, 2 -> draw-brush
        self.selection = list()
        self.selected_img = None

    @img_open
    def close_image(self, index):
        self.images[index].close_all_img()
        self.images = self.images[:index] + self.images[index+1:]
        self.select()
        self.task = 0

    def add_image(self, *args):
        self.images.append(ImageObject(*args))

    def get_img(self):
        page_num = self.parent.notebook.get_current_page()
        img = self.images[page_num].get_current_img()
        return img

    @img_open
    def apply_filter(self, action, parameter, func, value=None):
        func = eval(func)
        img = self.get_img()
        new_img = func(img, value) if value else func(img)
        self.do_change(new_img)

    def do_change(self, img):
        page_num = self.parent.notebook.get_current_page()
        self.parent.update_image(img)
        self.images[page_num].forget_img()
        self.images[page_num].add_img(img)
        self.images[page_num].increment_index()
        self.images[page_num].saved = False
        if self.images[page_num].get_n_img() > self.MAX_HIST:
            self.images[page_num].remove_first_img()
            self.images[page_num].decrement_index()

    @img_open
    def filter_with_params(self, action, parameter, params):
        func, title, limits = params
        params_dialog = dialog.params_dialog(self.parent, title, limits)
        value = params_dialog.get_values()
        if value:
            self.apply_filter(None, None, func, value)

    @img_open
    def history(self, action, parameter, num):
        page_num = self.parent.notebook.get_current_page()
        if self.images[page_num].get_n_img() >= 2:
            index_img = self.images[page_num].index
            if num == -1: # Undo:
                if index_img >= 1:
                    self.images[page_num].decrement_index()
                    img = self.images[page_num].get_current_img()
                    self.parent.update_image(img)
            else: # Redo:
                if index_img + 1 < self.images[page_num].get_n_img():
                    self.images[page_num].increment_index()
                    img = self.images[page_num].get_current_img()
                    self.parent.update_image(img)

    @img_open
    def select(self, action=None, parameter=None):
        if self.task != 0:
            if self.task == 1:
                page_num = self.parent.notebook.get_current_page()
                tmp_img = self.images[page_num].get_tmp_img()
                if tmp_img:
                    self.do_change(tmp_img)
                    self.images[page_num].tmp_img = None
            self.change_cursor(0)
            self.task = 0

    @img_open
    def draw(self, action, parameter):
        if self.task != 2:
            self.task = 2
            self.change_cursor(1)

    def get_vars(self, mouse_coords, is_tmp=False):
        """Return required variables."""
        page_num = self.parent.notebook.get_current_page()
        if is_tmp:
            img = self.images[page_num].get_tmp_img().copy()
        else:
            img = self.get_img().copy()
        tab = self.parent.notebook.get_nth_page(page_num)
        x_mouse = round(mouse_coords[0])
        y_mouse = round(mouse_coords[1])
        return [x_mouse, y_mouse], page_num, img

    def press_task(self, widget, event):
        mouse_coords, page_num, img = self.get_vars((event.x, event.y))
        if self.task == 0:
            self.selection = mouse_coords
            self.parent.update_image(img)
        elif self.task == 2 or (self.task == 1 and self.selected_img):
            self.move_task(event=event)

    def move_task(self, widget=None, event=None):
        mouse_coords, page_num, img = self.get_vars((event.x, event.y), True)
        if self.task == 0:
            draw_shape(img, 'rectangle', xy=[self.selection[0], self.selection[1], mouse_coords[0], mouse_coords[1]], outline='black')
            self.parent.update_image(img)
        elif self.task == 2:
            draw_point(img, mouse_coords)
            self.set_tmp_img(img)
        elif self.task == 1:
            self.paste(mouse_coords=mouse_coords)

    def release_task(self, widget, event):
        mouse_coords, page_num, img = self.get_vars((event.x, event.y), True)
        if self.task == 0:
            self.selection.extend(mouse_coords)
        elif self.task == 2:
            self.images[page_num].tmp_img = None
            self.do_change(img)

    def change_cursor(self, cursor):
        tab = self.parent.notebook.get_nth_page(self.parent.notebook.get_current_page())
        img = tab.img_widget.get_window()
        if cursor == 0:
            img.set_cursor(self.parent.default_cursor)
        elif cursor == 1:
            img.set_cursor(self.parent.draw_cursor)
        elif cursor == 2:
            img.set_cursor(self.parent.move_cursor)

    def set_tmp_img(self, img):
        self.parent.update_image(img)
        page_num = self.parent.notebook.get_current_page()
        self.images[page_num].tmp_img = img

    @img_open
    def copy(self, action=None, parameter=None):
        if self.selection != list():
            img = self.get_img()
            self.selected_img = img.crop(tuple(self.selection))

    @img_open
    def paste(self, action=None, parameter=None, mouse_coords=None):
        if self.selected_img:
            if self.task != 1:
                self.task = 1
                self.change_cursor(2)
                xy = (0, 0)
            else:
                xy = get_middle_mouse(self.selected_img.size, mouse_coords)
            new_img = self.get_img().copy()
            new_img.paste(self.selected_img, xy)
            self.set_tmp_img(new_img)

    @img_open
    def cut(self, action, parameter):
        if self.selection != list():
            self.copy()
            blank_img = Image.new('RGB', self.selected_img.size, 'white')
            img = self.get_img().copy()
            img.paste(blank_img, tuple(self.selection[:2]))
            self.do_change(img)

    @img_open
    def file_save(self, action, parameter):
        page_num = self.parent.notebook.get_current_page()
        if self.images[page_num].is_new_image:
            self.file_save_as()
        else:
            img = self.images[page_num].get_current_img()
            self.images[page_num].saved = True
            img.save(self.images[page_num].filename)

    @img_open
    def file_save_as(self, action=None, parameter=None):
        filename = dialog.file_dialog(self.parent, 'save')
        if filename:
            page_num = self.parent.notebook.get_current_page()
            img = self.images[page_num].get_current_img()
            img.save(filename)
            self.images[page_num].filename = filename
            page_num = self.parent.notebook.get_current_page()
            self.parent.notebook.get_nth_page(page_num).tab_label.set_label(path.basename(filename))
            self.images[page_num].saved = True

    @img_open
    def properties(self, action, parameter):
        page_num = self.parent.notebook.get_current_page()
        img_infos = get_infos(self.images[page_num])
        dialog.properties_dialog(self.parent, img_infos)
