#!/usr/bin/python

from PIL import Image
from os import path

from interface import dialog
from filters import base
from editor.image import ImageObject, Layer, Filter
from editor.tools import get_middle_mouse, get_infos
from editor.draw import draw_rectangle, draw_ellipse

def img_open(func):
    def inner(self, *args, **kwargs):
        if self.image:
            return func(self, *args, **kwargs)
    return inner


class Editor(object):
    def __init__(self, win, tab, img, filename, saved):
        super(Editor, self).__init__()
        self.win = win
        self.tab = tab

        self.image = ImageObject(img, filename, saved)
        self.MAX_HIST = 20

        self.task = 0  # 0 -> select, 1 -> paste, 2 -> pencil
        self.selection = list()
        self.selected_img = None

        # Settings
        self.pencil_shape = 'ellipse'
        self.pencil_color = 'black'
        self.pencil_size = 8

    def close_image(self):
        self.image = None
        self.select()
        self.task = 0

    def do_change(self, img):
        self.tab.update_image(img)
        self.image.new_layer()
        self.image.saved = False

    def apply_filter(self, func, params=None):
        if params:
            params_dialog = dialog.params_dialog(self.win, *params)
            value = params_dialog.get_values()
            new_img = getattr(base, func)(self.image.get_current_img(), value)
        else:
            new_img = getattr(base, func)(self.image.current_img)
        self.do_change(new_img)

    def history(self, num):
        print('history')
        print(self.image)
        if len(self.image.layers) >= 2:
            if num == -1: # Undo:
                if self.image.index >= 1:  # != 0  # > 0
                    self.image.undo()
                    self.tab.update_image(self.image.current_img)
            else: # Redo:
                if self.image.index < len(self.image.layers):
                    self.image.redo()
                    self.tab.update_image(self.image.current_img)
        print(self.image)

    def select(self):
        if self.task != 0:
            if self.task == 1:  # paste
                tmp_img = self.image.get_tmp_img()
                if tmp_img:  # is not None:
                    self.do_change(tmp_img)
                    self.image.tmp_img = None
            self.change_cursor(0)
            self.task = 0

    def pencil(self):
        if self.task != 2:
            self.task = 2
            self.change_cursor(1)

    def get_vars(self, mouse_coords, is_tmp=False):
        """Return required variables."""
        if is_tmp:
            img = self.image.get_tmp_img().copy()  # need to be change (remove .copy())
        else:
            img = self.image.current_img.copy()
        return list(map(round, mouse_coords)), img

    def press_task(self, widget, event):
        mouse_coords, img = self.get_vars((event.x, event.y))
        if self.task == 0:
            self.selection = mouse_coords
            self.tab.update_image(img)
        elif (self.task == 1 and self.selected_img):
            self.move_task(event=event)
        elif self.task == 2:  # pencil
            print('pencil press_task')
            layer = Layer(self.pencil_shape, list(), self.pencil_size, self.pencil_color)
            print('press_task')
            print(type(layer))
            self.image.tmp_layer = layer
            self.image.tmp_img = self.image.current_img  # bad!
            self.move_task(event=event)

    def move_task(self, widget=None, event=None):
        mouse_coords, img = self.get_vars((event.x, event.y), True)
        if self.task == 0:  # select
            top_left = (self.selection[0], self.selection[1])
            bottom_right = (mouse_coords[0], mouse_coords[1])
            coords = (top_left, bottom_right)
            draw_rectangle(img, coords, False, 'black', 0)
            self.tab.update_image(img)
        elif self.task == 1:
            self.paste(mouse_coords=mouse_coords)
        elif self.task == 2:  # pencil
            top_left = (mouse_coords[0], mouse_coords[1])
            bottom_right = (mouse_coords[0], mouse_coords[1])
            coords = (top_left, bottom_right)
            self.image.add_coords(coords)
            img = self.image.tmp_layer.execute(self.image.current_img)
            self.set_tmp_img(img)

    def release_task(self, widget, event):
        mouse_coords, img = self.get_vars((event.x, event.y), True)
        if self.task == 0:
            self.selection.extend(mouse_coords)
        elif self.task == 2:  # pencil
            self.do_change(img)
            self.image.tmp_img = None

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

    def copy(self):
        if self.selection != list():
            self.selected_img = self.image.current_img.crop(tuple(self.selection))

    def paste(self, mouse_coords=None):
        if self.selected_img:
            if self.task != 1:
                self.task = 1
                self.change_cursor(3)
                xy = (0, 0)
            else:
                xy = get_middle_mouse(self.selected_img.size, mouse_coords)
            new_img = self.image.current_img.copy()
            new_img.paste(self.selected_img, xy)
            self.set_tmp_img(new_img)

    def cut(self):
        if self.selection != list():
            self.copy()
            blank_img = Image.new('RGBA', self.selected_img.size, (255, 255, 255, 0))
            img = self.image.current_img.copy()
            img.paste(blank_img, tuple(self.selection[:2]))
            self.do_change(img)

    def save(self):
        if path.isfile(self.image.filename):
            img = self.image.current_img
            img.save(self.image.filename)
            self.image.saved = True
        else:
            self.save_as()

    def save_as(self):
        filename = dialog.file_dialog(self.win, 'save', path.basename(self.image.filename))
        if filename:
            img = self.image.current_img
            img.save(filename)
            self.image.filename = filename
            self.tab.tab_label.set_title(path.basename(filename))
            self.image.saved = True

    def details(self):
        img_infos = get_infos(self.image)
        dialog.details_dialog(self.win, img_infos)
