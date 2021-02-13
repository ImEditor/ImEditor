import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from PIL import Image
from os import stat, path
from datetime import datetime

from .dialog import *
from .base import *
from .image import ImageObject
from .draw import draw_rectangle, draw_ellipse
from .tools import pil_to_pixbuf

class Editor(object):
    def __init__(self, tab, img, filename, saved):
        super(Editor, self).__init__()
        self.win = tab.win
        self.tab = tab

        self.image = ImageObject(img, filename, saved)

        # History
        self.MAX_HIST = 100

        # Tasks
        self.task = 0  # 0 -> select, 1 -> paste, 2 -> draw

        # Coords of selected region
        self.selection = list()

        # Pencil settings
        self.pencil_shape = 0 # 0 -> ellipse, 1 -> square
        self.pencil_color = 'black'
        self.pencil_size = 8

        # Temp vars
        self.left_button_pressed = False

        # Cursors
        display = Gdk.Display.get_default()
        try:
            self.cursors = {
                'default': Gdk.Cursor.new_from_name(display, 'default'),
                'draw': Gdk.Cursor.new_for_display(display, Gdk.CursorType.PENCIL),
                'move': Gdk.Cursor.new_from_name(display, 'move')
            }
        except TypeError as e:
            self.cursors = None

    def change_task(self, task='select'):
        """Change active task and its cursor"""
        if task == 'select':
            self.task = 0
            self.change_cursor('default')
        elif task == 'paste':
            self.task = 1
            self.change_cursor('move')
        elif task == 'draw':
            self.task = 2
            self.change_cursor('draw')

    def change_cursor(self, cursor):
        """Change cursor that hovers the image"""
        img_widget = self.tab.img_widget.get_window()
        if img_widget and self.cursors:
            img_widget.set_cursor(self.cursors[cursor])

    def do_tmp_change(self, img):
        """Update displayed image without modifying the history"""
        self.tab.update_image(img, True)
        self.image.tmp_img = img

    def do_change(self, img):
        """Update displayed image and save it in the history"""
        if self.image.tmp_img:
            self.image.tmp_img = None  # remove tmp image
        # Update image
        self.tab.update_image(img)
        # Save it in the history
        self.image.forget_img()
        self.image.add_img(img)
        self.image.increment_index()
        self.image.saved = False
        if self.image.get_n_img() > self.MAX_HIST:
            self.image.remove_first_img()
            self.image.decrement_index()

    def undo(self):
        """Go to the previous image in the history"""
        if self.image.get_n_img() > 1:
            if self.image.index > 0:
                self.image.decrement_index()
                self.tab.update_image(self.image.get_current_img())

    def redo(self):
        """Go to the next image of the history"""
        if self.image.get_n_img() > 1:
            if self.image.index + 1 < self.image.get_n_img():
                self.image.increment_index()
                self.tab.update_image(self.image.get_current_img())

    def apply_filter(self, func, value=None):
        """Apply a filter from filters/base.py"""
        if value:
            img = globals()[func](self.image.get_current_img(), value)
        else:
            img = globals()[func](self.image.get_current_img())
        self.do_change(img)

    def apply_filter_dialog(self, func, params):
        """Apply a filter from filters/base.py that need a GUI"""
        dialog = params_dialog(self.win, *params)
        value = dialog.get_values()
        if value:
            self.apply_filter(func, value)

    def handle_event(self, widget, event, task):
        """Call the event with the needed vars"""
        # Only allow the left mouse button to do actions
        if hasattr(event, 'button') and event.button != 1:
            return
        # Get the good image
        if not self.image.tmp_img:
            img = self.image.get_current_img()
        else:
            img = self.image.tmp_img
        # Handle mouse coords
        x, y = event.x, event.y
        if self.tab.zoom_level != 100:
            x *= self.image.size[0] / self.tab.disp_width
            y *= self.image.size[1] / self.tab.disp_height
        mouse_coords = [round(x), round(y)]
        # Call the good function to handle the event
        getattr(self, task + '_task')(img.copy(), mouse_coords)

    def press_task(self, img, mouse_coords):
        """Press event"""
        self.left_button_pressed = True
        if self.task == 0:
            self.selection = mouse_coords
            self.tab.update_image(img)
        elif (self.task == 1 and self.selection):
            self.move_task(img, mouse_coords)
        elif self.task == 2:
            self.last_drawn_point = mouse_coords
            self.move_task(img, mouse_coords)

    def move_task(self, img, mouse_coords):
        """Move event"""
        if not self.left_button_pressed:  # need that press_task have been called
            return
        # Ensure that coords are in the image area
        for i in range(2):
            # Higher than the image
            if mouse_coords[i] > self.image.size[i]:
                mouse_coords[i] = self.image.size[i]
            # Lower than 0
            elif mouse_coords[i] < 0:
                mouse_coords[i] = 0
        if self.task == 0:
            coords = (self.selection, mouse_coords)
            draw_rectangle(img, coords, 0, outline_color='black')
            self.tab.update_image(img)
        elif self.task == 1:
            self.paste(mouse_coords)
        elif self.task == 2:
            coords = ((mouse_coords[0], mouse_coords[1]),
                (mouse_coords[0], mouse_coords[1]))
            if self.pencil_shape == 0:
                new_coords = draw_ellipse(img, coords, self.pencil_size, self.pencil_color)
            elif self.pencil_shape == 1:
                new_coords = draw_rectangle(img, coords, self.pencil_size, self.pencil_color)

            self.do_tmp_change(img)

    def release_task(self, img, mouse_coords):
        """Release event"""
        if self.task == 0 and mouse_coords != self.selection:
            m0, m1 = mouse_coords[0], mouse_coords[1]
            s0, s1 = self.selection[0], self.selection[1]
            # Allow selection from all corners
            if m0 >= s0 and m1 > s1:  # top-left
                self.selection = [s0, s1, m0, m1]
            elif m0 <= s0 and m1 <= s1:  # bottom-right
                self.selection = [m0, m1, s0, s1]
            elif m0 >= s0 and m1 <= s1:  # bottom-left
                self.selection = [s0, m1, m0, s1]
            elif m0 <= s0 and m1 >= s1:  # top-right
                self.selection = [m0, s1, s0, m1]
        elif self.task == 1:
            self.do_change(img)
            self.change_task()
            self.selection = list()
        elif self.task == 2:
            self.do_change(img)
        self.left_button_pressed = False

    def copy(self):
        """Copy a part of/or the entire image"""
        # Intern copy
        img = self.image.get_current_img().copy()
        if len(self.selection) == 4:  # a part of the image is selected
            img = img.crop(tuple(self.selection))
        else:  # copy the entire image
            self.selection = [0, 0]
        self.win.selected_img = img
        # Clipboard copy
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        pixbuf = pil_to_pixbuf(img)
        clipboard.set_image(pixbuf)

    def paste(self, mouse_coords=None):
        """Paste the copied image"""
        if self.win.selected_img:
            if self.task != 1:
                self.change_task('paste')
            if mouse_coords:
                xy = get_middle_mouse(self.win.selected_img.size, mouse_coords)
            else:
                xy = (0, 0)
            img = self.image.get_current_img().copy()
            img.paste(self.win.selected_img, xy)
            self.do_tmp_change(img)
            self.selection = list()

    def cut(self):
        """Copy in removing the selected part"""
        self.copy()
        img = self.image.get_current_img().copy()
        blank_img = Image.new(img.mode, self.win.selected_img.size,
            'rgba(255, 255, 255, 0)')
        img.paste(blank_img, tuple(self.selection[:2]))
        self.do_change(img)
        self.selection = list()

    def crop(self):
        """Crop an image"""
        if len(self.selection) == 4:  # a part of the image is selected
            img = self.image.get_current_img().crop(tuple(self.selection))
            self.do_change(img)

    def save(self):
        """Save the image"""
        if path.isfile(self.image.filename):
            img = self.image.get_current_img()
            img.save(self.image.filename)
            self.image.saved = True
        else:
            self.save_as()

    def save_as(self):
        """Ask where to save the image"""
        filename = file_dialog(self.win, 'save', path.basename(self.image.filename))
        if filename:
            img = self.image.get_current_img()
            img.save(filename)
            self.win.filenames.append(filename)
            self.image.filename = filename
            self.tab.tab_label.set_title(path.basename(filename))
            self.win.set_window_title(self.tab)
            self.image.saved = True

    def details(self):
        """Get informations about the image"""
        img_infos = get_infos(self.image.get_current_img(), self.image.filename)
        details_dialog(self.win, img_infos)

    def close_image(self):
        """Close the image and all its history"""
        self.image.close_all_img()


def get_middle_mouse(size, mouse_coords):
    x = mouse_coords[0] - (size[0] / 2)
    y = mouse_coords[1] - (size[1] / 2)
    return (round(x), round(y))


def get_infos(img, filename):
    """Fetch informations about an image"""
    # Basic infos
    img_infos = {
        'name': path.basename(filename),
        'mode': img.mode,
        'size': '{} x {} pixels'.format(str(img.width), str(img.height))
    }
    # Infos available only if the image is saved on the disk
    if path.isfile(filename):
        img_stat = stat(filename)
        img_infos['weight'] = '{}ko ({}o)'.format(str(round(img_stat.st_size / 1000, 2)),
                                                    str(round(img_stat.st_size, 2)))
        img_infos['last_change'] = datetime.fromtimestamp(img_stat.st_mtime).strftime('%d/%m/%Y %Hh%M')
    return img_infos
