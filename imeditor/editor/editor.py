#!/usr/bin/python

from PIL import Image
from os import path

from interface import dialog
from filters import base
from editor.image import ImageObject
from editor.tools import get_middle_mouse, get_infos
from editor.draw import draw_rectangle, draw_ellipse


def img_open(func):
    def inner(self, *args, **kwargs):
        if self.image:
            return func(self, *args, **kwargs)
    return inner


class Editor(object):
    def __init__(self, win, tab):
        super(Editor, self).__init__()
        self.win = win
        self.tab = tab

        self.image = None
        self.MAX_HIST = 10

        self.task = 0  # 0 -> select, 1 -> paste, 2 -> pencil
        self.selection = list()
        self.selected_img = None

        # Settings
        self.color = 'black'
        self.size = 8

    def add_image(self, *args):
        self.image = ImageObject(*args)

    @img_open
    def close_image(self, index):
        self.image.close_all_img()
        self.image = None
        self.select()
        self.task = 0

    def do_change(self, img):
        self.tab.update_image(img)
        self.image.forget_img()
        self.image.add_img(img)
        self.image.increment_index()
        self.image.saved = False
        if self.image.get_n_img() > self.MAX_HIST:
            self.image.remove_first_img()
            self.image.decrement_index()

    @img_open
    def apply_filter(self, func, value=None):
        func = eval(func)
        if value:
            new_img = func(self.image.get_current_img(), value)
        else:
            new_img = func(self.image.get_current_img())
        self.do_change(new_img)

    @img_open
    def apply_filter_with_params(self, params):
        func, title, limits = params
        params_dialog = dialog.params_dialog(self.win, title, limits)
        value = params_dialog.get_values()
        if value:
            self.apply_filter(func, value)

    @img_open
    def history(self, num):
        if self.image.get_n_img() >= 2:
            index_img = self.image.index
            if num == -1: # Undo:
                if index_img >= 1:
                    self.image.decrement_index()
                    img = self.image.get_current_img()
                    self.tab.update_image(img)
            else: # Redo:
                if index_img + 1 < self.image.get_n_img():
                    self.image.increment_index()
                    img = self.image.get_current_img()
                    self.tab.update_image(img)

    @img_open
    def select(self):
        if self.task != 0:
            if self.task == 1:
                tmp_img = self.image.get_tmp_img()
                if tmp_img:
                    self.do_change(tmp_img)
                    self.image.tmp_img = None
            self.change_cursor(0)
            self.task = 0

    @img_open
    def pencil(self):
        if self.task != 2:
            self.task = 2
            self.change_cursor(1)

    def get_vars(self, mouse_coords, is_tmp=False):
        """Return required variables."""
        if is_tmp:
            img = self.image.get_tmp_img().copy()
        else:
            img = self.image.get_current_img().copy()
        x_mouse = round(mouse_coords[0])
        y_mouse = round(mouse_coords[1])
        return [x_mouse, y_mouse], img

    def press_task(self, widget, event):
        mouse_coords, img = self.get_vars((event.x, event.y))
        if self.task == 0:
            self.selection = mouse_coords
            self.tab.update_image(img)
        elif (self.task == 1 and self.selected_img) or self.task == 2:
            self.move_task(event=event)

    def move_task(self, widget=None, event=None):
        mouse_coords, img = self.get_vars((event.x, event.y), True)
        if self.task == 0:
            top_left = (self.selection[0], self.selection[1])
            bottom_right = (mouse_coords[0], mouse_coords[1])
            coords = (top_left, bottom_right)
            draw_rectangle(img, coords, False, self.color, 0)
            self.tab.update_image(img)
        elif self.task == 1:
            self.paste(mouse_coords=mouse_coords)
        elif self.task == 2:
            top_left = (mouse_coords[0], mouse_coords[1])
            bottom_right = (mouse_coords[0], mouse_coords[1])
            coords = (top_left, bottom_right)
            draw_ellipse(img, coords, True, self.color, self.size)
            self.set_tmp_img(img)

    def release_task(self, widget, event):
        mouse_coords, img = self.get_vars((event.x, event.y), True)
        if self.task == 0:
            self.selection.extend(mouse_coords)
        elif self.task == 2:
            self.image.tmp_img = None
            self.do_change(img)

    def change_cursor(self, cursor):
        img = self.tab.img_widget.get_window()
        if cursor == 0:
            img.set_cursor(self.win.default_cursor)
        elif cursor == 1:
            img.set_cursor(self.win.draw_cursor)
        elif cursor == 3:
            img.set_cursor(self.win.move_cursor)

    def set_tmp_img(self, img):
        self.tab.update_image(img)
        self.image.tmp_img = img

    @img_open
    def copy(self):
        if self.selection != list():
            self.selected_img = self.image.get_current_img().crop(tuple(self.selection))

    @img_open
    def paste(self, mouse_coords=None):
        if self.selected_img:
            if self.task != 1:
                self.task = 1
                self.change_cursor(2)
                xy = (0, 0)
            else:
                xy = get_middle_mouse(self.selected_img.size, mouse_coords)
            new_img = self.image.get_current_img().copy()
            new_img.paste(self.selected_img, xy)
            self.set_tmp_img(new_img)

    @img_open
    def cut(self):
        if self.selection != list():
            self.copy()
            blank_img = Image.new('RGBA', self.selected_img.size, (255, 255, 255, 0))
            img = self.image.get_current_img().copy()
            img.paste(blank_img, tuple(self.selection[:2]))
            self.do_change(img)

    @img_open
    def save(self):
        if path.isfile(self.image.filename):
            img = self.image.get_current_img()
            self.image.saved = True
            img.save(self.image.filename)
        else:
            self.file_save_as()

    @img_open
    def save_as(self):
        filename = dialog.file_dialog(self.win, 'save', path.basename(self.image.filename))
        if filename:
            img = self.image.get_current_img()
            img.save(filename)
            self.image.filename = filename
            self.tab.set_label(path.basename(filename))
            self.image.saved = True

    @img_open
    def details(self):
        img_infos = get_infos(self.image)
        dialog.details_dialog(self.win, img_infos)
