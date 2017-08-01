#!/usr/bin/python

from editor.draw import draw_rectangle, draw_ellipse

class ImageObject(object):
    def __init__(self, img, filename, saved):
        print('new image object!')
        super(ImageObject, self).__init__()
        self.layers = list()  # 20 max ( 5 for tests)
        self.redo_stack = list()
        self.undo_stack = list()
        self.tmp_layer = str()
        self.filename = filename
        self.index = 0  # the size of the layers list
        self.saved = saved
        self.tmp_img = img  # for select task
        self.current_img = img.copy()
        self.img_original = img.copy()

    def __str__(self):
        result = 'ImageObject, '
        result += str(self.layers) + '\n'
        result += str(self.index)
        return result

    def get_tmp_img(self):
        if self.tmp_img:
            return self.tmp_img
        else:
            return self.current_img

    def add_coords(self, coords):
        self.tmp_layer.add_coords(coords)
        # make ligne to avoid blanks

    def apply_layer(self):
        return self.tmp_layer.execute(self.current_img)

    def new_layer(self):
        print('new_layer')
        print(type(self.tmp_layer))
        self.layers.append(self.tmp_layer)
        self.index += 1
        self.img_original.save('org.png')
        ### draw an image modify itself so even if self.img_original isn't redifined, it change at each new layer
        # TODO: MAX_HIST

    def undo(self):
        # Execute all layers to the original image.
        print('undo')
        self.index -= 1
        img = self.img_original.copy()
        img.save('org.png')
        layer_redone = 0
        for layer in self.layers:
            if layer_redone < self.index:
                img = layer.execute(img)
                layer_redone += 1
            else:
                break
                print('break')
            print(layer_redone)
            img.save(str(layer_redone) + '.png')
        self.current_img = img
        img.save('fin.png')

    def redo(self):
        self.index += 1
        self.current_img = self.layers[self.index -1].execute(self.current_img)

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
    def __init__(self, func, values):
        super(Filter, self).__init__()
        self.func = func
        self.values = values

    def execute(self, img):
        """Apply the filter to the given im, return it."""
        pass
