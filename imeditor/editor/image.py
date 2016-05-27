# -*- coding: utf-8 -*-
#!/usr/bin/python3

class ImageObject(object):
    def __init__(self, img, filename, index, saved, is_new_image=False):
        super(ImageObject, self).__init__()
        self.images = [img]
        self.filename = filename
        self.index = index
        self.saved = saved
        self.is_new_image = is_new_image
        self.tmp_img = None

    def __str__(self):
        result = str(self.images) + '\n'
        result += str(self.index)
        return result

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

    def set_saved(self, saved):
        self.saved = saved

    def get_saved(self):
        return self.saved

    def get_is_new_image(self):
        return self.is_new_image

    def set_tmp_img(self, tmp_img):
        self.tmp_img = tmp_img

    def get_tmp_img(self):
        if self.tmp_img:
            return self.tmp_img
        else:
            return self.get_current_img()

    def add_img(self, img):
        self.images.append(img)

    def get_current_img(self):
        return self.images[self.index]

    def remove_first_img(self):
        self.images = self.images[1:]

    def close_all_img(self):
        for img in self.images:
            img.close()

    def increment_index(self):
        self.index += 1

    def decrement_index(self):
        self.index -= 1

    def get_n_img(self):
        return len(self.images)

    def forget_img(self):
        """Remove all images after the modified image in history."""
        self.images = self.images[:self.index + 1]
