#!/usr/bin/python3

from gi.repository import Gtk, GdkPixbuf
from io import BytesIO

def create_pixbuf(img):
    file1 = BytesIO()
    img.save(file1, "ppm")
    contents = file1.getvalue()
    file1.close()
    loader = GdkPixbuf.PixbufLoader()
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()

    return pixbuf

def about():
    dialog = Gtk.AboutDialog()
    dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file('assets/icons/imeditor.png'))
    dialog.set_program_name('ImEditor')
    dialog.set_version('0.1')
    dialog.set_website('https://github.com/ImEditor')
    dialog.set_authors(['Nathan Seva', 'Hugo Posnic'])
    dialog.set_comments('GTK Linux Image Editor ')
    dialog.set_license('Distributed under the GNU GPL(v3) license. \n\n https://github.com/ImEditor/ImEditor/blob/master/LICENSE')

    dialog.run()
    dialog.destroy()
