#!/usr/bin/env python3


class ImageObject(object):
    def __init__(self, img, filename, saved):
        super(ImageObject, self).__init__()
        self.images = [img]
        self.filename = filename
        self.size = img.size
        self.saved = saved
        self.index = 0
        self.tmp_img = None

    def add_img(self, img):
        self.images.append(img)

    def get_current_img(self):
        return self.images[self.index]

    def remove_first_img(self):
        self.images = self.images[1:]

    def increment_index(self):
        self.index += 1

    def decrement_index(self):
        self.index -= 1

    def get_n_img(self):
        return len(self.images)

    def forget_img(self):
        """Remove all images after the modified image in history."""
        self.images = self.images[:self.index + 1]

    def close_all_img(self):
        for img in self.images:
            img.close()
