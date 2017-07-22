#!/usr/bin/python

from editor.draw import draw_rectangle, draw_ellipse

class ImageObject(object):
    def __init__(self, img, filename, saved):
        super(ImageObject, self).__init__()
        self.layers = list()  # 20 max ( 5 for tests)
        self.tmp_layer = None
        self.filename = filename
        self.index = 0
        self.saved = saved
        self.tmp_img = None  # for select task
        self.current_img = img
        self.img_original = img

    def __str__(self):
        result = str(self.layers) + '\n'
        result += str(self.index)
        return result

    def get_tmp_img(self):
        if self.tmp_img:
            return self.tmp_img
        else:
            return self.current_img

    def remove_first_layer(self):
        self.layers = self.layers[1:]

    def apply_layer(self):
        return self.tmp_layer.execute(self.current_img)

    def new_layer(self):
        self.layers.append(self.tmp_layer)
        self.index += 1
        self.layers = self.layers[:self.index]
        if len(self.layers) >= 5:  # 20
            self.layers = self.layers[1:]
            self.index -= 1

    def undo(self):
        """Execute all layers to the original image."""
        if self.index >= 1:
            self.index -= 1
        img = self.img_original
        for layer in self.layers:
            img = layer.execute(img)
        self.current_img = img

    def redo(self):
        self.index += 1
        if len(self.layers) >= 5:  # 20
            self.layers = self.layers[:self.index]
        self.current_img = self.layers[index].execute(self.current_img)

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
        elif self.pencil_shape == 'rectangle':
            for coords in self.location:
                draw_rectangle(img, coords, True, self.color, self.size)
        return img

class Filter(object):
    def __init__(self, func, values):
        super(Filter, self).__init__()
        self.func = func
        self.values = values

    def execute(self, img):
        """Apply the filter to the given im, return it."""
