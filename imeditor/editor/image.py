#!/usr/bin/python

from editor.draw import draw_rectangle, draw_ellipse

class ImageObject(object):
    def __init__(self, img, filename, saved):
        print('new image object!')
        super(ImageObject, self).__init__()
        self.redo_stack = list()
        self.undo_stack = list()
        self.filename = filename
        self.saved = saved
        self.tmp_img = img  # for select task
        self.current_img = img.copy()

    def __str__(self):
        result = 'ImageObject, '
        result += str(self.redo_stack) + '\n'
        result += str(self.undo_stack) + '\n'
        return result

    def get_tmp_img(self):
        if self.tmp_img:
            return self.tmp_img
        else:
            return self.current_img

    def new_filter(self, func, value=None):
        print('filter')
        layer = Filter(func, value)
        layer.execute(self.current_img)
        self.undo_stack.append(layer)
        self.redo_stack.clear()
        print(layer)

    def undo(self):
        if len(self.undo_stack) > 0:
            layer_undo = self.undo_stack.pop()
            self.redo_stack.append(layer_undo)
            layer_undo.reverse(self.current_img)

    def redo(self):
        if len(self.redo_stack) > 0:
            layer_redo = self.redo_stack.pop()
            self.undo_stack.append(layer_redo)
            layer_redo.execute(self.current_img)

class Task(object):
    def __init__(self):
        super(Task, self).__init__()

    def execute(self, img):
        pass

    def reverse(self, img):
        pass

class Layer(object):
    def __init__(self, shape=None, location=list(), size=8, color='#000000'):
        super(Layer, self).__init__()
        # shape : ellipse or rectangle
        self.shape = shape
        # location : a list of tuple to localize pixels
        self.location = location
        # size : Editor.pencil_size
        self.size = size
        self.color = color

    def add_coords(self, coords):
        self.location.append(coords)

    def execute(self, img):
        """Apply the layer to the given img, return it."""
        if self.shape == 'ellipse':
            for coords in self.location:
                draw_ellipse(img, coords, True, self.color, self.size)
        elif self.shape == 'rectangle':
            for coords in self.location:
                draw_rectangle(img, coords, True, self.color, self.size)
        return img

class Filter(object):
    def __init__(self, func, value):
        super(Filter, self).__init__()
        self.func = func
        self.value = value

    def execute(self, img):
        """Apply the filter to the given im, return it."""
        if self.value:
            self.func(img, self.value)
        else:
            self.func(img)

    def reverse(self, img):
        if self.value:
            self.func(img, self.value, True)
        else:
            self.func(img, True)
