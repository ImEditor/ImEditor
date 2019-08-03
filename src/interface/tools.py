import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib


def create_empty_pixbuf(img):
    if img.mode == 'RGB':
        alpha = False
    elif img.mode == 'RGBA':
        alpha = True
    return GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, alpha, 8,
        img.width, img.height)

def pil_to_pixbuf(img):
    """Convert the PIL image to a Pixbuf usable by Gtk"""
    data = GLib.Bytes.new(img.tobytes())
    w, h = img.size
    if img.mode == 'RGB':
        alpha = False
        rowstrides = 3
    elif img.mode == 'RGBA':
        alpha = True
        rowstrides = 4
    return GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
        alpha, 8, w, h, w * rowstrides)


def add_filechooser_filters(dialog):
    all_images = Gtk.FileFilter()
    all_images.set_name(_("All images"))
    all_images.add_mime_type('image/bmp')
    all_images.add_mime_type('image/jpeg')
    all_images.add_mime_type('image/png')
    all_images.add_mime_type('image/webp')
    all_images.add_mime_type('image/ico')

    bmp_images = Gtk.FileFilter()
    bmp_images.set_name(_("BMP images"))
    bmp_images.add_mime_type('image/bmp')

    png_images = Gtk.FileFilter()
    png_images.set_name(_("PNG images"))
    png_images.add_mime_type('image/png')

    jpeg_images = Gtk.FileFilter()
    jpeg_images.set_name(_("JPEG images"))
    jpeg_images.add_mime_type('image/jpeg')

    webp_images = Gtk.FileFilter()
    webp_images.set_name(_("WEBP images"))
    webp_images.add_mime_type('image/webp')

    ico_images = Gtk.FileFilter()
    ico_images.set_name(_("ICO images"))
    ico_images.add_mime_type('image/ico')

    dialog.add_filter(all_images)
    dialog.add_filter(png_images)
    dialog.add_filter(jpeg_images)
    dialog.add_filter(webp_images)
    dialog.add_filter(ico_images)


class SpinButton(Gtk.SpinButton):
    def __init__(self, default, min_value, max_value, step=20, page=40):
        Gtk.SpinButton.__init__(self)
        self.set_digits(0)
        self.set_numeric(False)
        self.set_range(min_value, max_value)
        self.set_value(default)
        self.set_increments(step, page)
