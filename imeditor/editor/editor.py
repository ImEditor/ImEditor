#!/usr/bin/python

from PIL import Image
from os import path

from interface import dialog
from filters import base
from editor.image import ImageObject
from editor.tools import get_middle_mouse, get_infos
from editor.draw import draw_rectangle, draw_ellipse


class Editor(object):
    def __init__(self, win, tab, img, filename, saved):
        super(Editor, self).__init__()
        self.win = win
        self.tab = tab

        self.image = ImageObject(img, filename, saved)

        # History
        self.MAX_HIST = 20

        # Tasks
        self.task = 0  # 0 -> select, 1 -> paste, 2 -> pencil
        self.selection = list()
        self.selected_img = None

        # Pencil settings
        self.pencil_shape = 'ellipse'
        self.pencil_color = 'black'
        self.pencil_size = 8

    def do_tmp_change(self, img):
        self.tab.update_image(img)
        self.image.tmp_img = img

    def do_change(self, img):
        self.tab.update_image(img)
        self.image.forget_img()
        self.image.add_img(img)
        self.image.increment_index()
        self.image.saved = False
        if self.image.get_n_img() > self.MAX_HIST:
            self.image.remove_first_img()
            self.image.decrement_index()

    def undo(self):
        if self.image.get_n_img() >= 2:
            index_img = self.image.index
            if index_img >= 1:
                self.image.decrement_index()
                img = self.image.get_current_img()
                self.tab.update_image(img)

    def redo(self):
        if self.image.get_n_img() >= 2:
            index_img = self.image.index
            if index_img + 1 < self.image.get_n_img():
                self.image.increment_index()
                img = self.image.get_current_img()
                self.tab.update_image(img)

    def apply_filter(self, func, params=None):
        if params:
            params_dialog = dialog.params_dialog(self.win, *params)
            value = params_dialog.get_values()
            if value:
                new_img = getattr(base, func)(self.image.get_current_img(), value)
                self.do_change(new_img)
        else:
            new_img = getattr(base, func)(self.image.get_current_img())
            self.do_change(new_img)

    def select(self):
        if self.task != 0:
            if self.task == 1:
                tmp_img = self.image.get_tmp_img()
                if tmp_img:
                    self.do_change(tmp_img)
                    self.image.tmp_img = None
            self.change_cursor('default')
            self.task = 0

    def pencil(self):
        if self.task != 2:
            self.task = 2
            self.change_cursor('draw')

    def handle_event(self, widget, event, task):
        """Return required variables."""
        img = self.image.get_tmp_img().copy()
        mouse_coords = [round(event.x), round(event.y)]
        getattr(self, task + "_task")(img, mouse_coords)

    def press_task(self, img, mouse_coords):
        if self.task == 0:
            self.selection = mouse_coords
            self.tab.update_image(img)
        elif (self.task == 1 and self.selected_img) or self.task == 2:
            self.move_task(img, mouse_coords)

    def move_task(self, img, mouse_coords):
        if self.task == 0:
            top_left = (self.selection[0], self.selection[1])
            bottom_right = (mouse_coords[0], mouse_coords[1])
            coords = (top_left, bottom_right)
            draw_rectangle(img, coords, 0, outline_color='black')
            self.tab.update_image(img)
        elif self.task == 1:
            self.paste(mouse_coords=mouse_coords)
        elif self.task == 2:
            coords = (mouse_coords[0], mouse_coords[1])
            coords = (coords, coords)
            if self.pencil_shape == 'ellipse':
                draw_ellipse(img, coords, self.pencil_size, self.pencil_color)
            elif self.pencil_shape == 'rectangle':
                draw_rectangle(img, coords, self.pencil_size, self.pencil_color)
            self.do_tmp_change(img)

    def release_task(self, img, mouse_coords):
        if self.task == 0:
            self.selection.extend(mouse_coords)
        elif self.task == 2:
            self.image.tmp_img = None
            self.do_change(img)

    def change_cursor(self, cursor):
        img = self.tab.img_widget.get_window()
        img.set_cursor(self.win.cursors[cursor])

    def copy(self):
        if self.selection != list():
            self.selected_img = self.image.get_current_img().crop(tuple(self.selection))

    def paste(self, mouse_coords=None):
        if self.selected_img:
            if self.task != 1:
                self.task = 1
                self.change_cursor('move')
                xy = (0, 0)
            else:
                xy = get_middle_mouse(self.selected_img.size, mouse_coords)
            new_img = self.image.get_current_img().copy()
            new_img.paste(self.selected_img, xy)
            self.do_tmp_change(new_img)

    def cut(self):
        if self.selection != list():
            self.copy()
            blank_img = Image.new('RGBA', self.selected_img.size, (255, 255, 255, 0))
            img = self.image.get_current_img().copy()
            img.paste(blank_img, tuple(self.selection[:2]))
            self.do_change(img)

    def save(self):
        if path.isfile(self.image.filename):
            img = self.image.get_current_img()
            img.save(self.image.filename)
            self.image.saved = True
        else:
            self.save_as()

    def save_as(self):
        filename = dialog.file_dialog(self.win, 'save', path.basename(self.image.filename))
        if filename:
            img = self.image.get_current_img()
            img.save(filename)
            self.image.filename = filename
            self.tab.tab_label.set_title(path.basename(filename))
            self.image.saved = True

    def details(self):
        img_infos = get_infos(self.image.get_current_img(), self.image.filename)
        dialog.details_dialog(self.win, img_infos)

    def close_image(self):
        self.image.close_all_img()
