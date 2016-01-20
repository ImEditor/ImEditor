#!/usr/bin/python3

from gi.repository import Gtk, Gdk, GdkPixbuf
import sys
from PIL import Image
from io import BytesIO
from os import path

from interface.tabs import TabLabel
from interface.menus import create_menus

class App(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='ImEditor')
        self.set_default_size(700, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('delete-event', self.quit_app)

        grid = Gtk.Grid()
        self.add(grid)

        menus = create_menus(self)
        grid.add(menus[0])  # Menu
        grid.attach(menus[1], 0, 0, 1, 1)  # Toolbar
        # Tabs:
        self.notebook = Gtk.Notebook()
        grid.attach(self.notebook, 0, 1, 1, 1)

        self.images = list()  # List of PIL images.

    def quit_app(self, _, __):
        Gtk.main_quit()

    def open_file(self, *args):
        dialog = Gtk.FileChooserDialog('Choisissez un fichier', self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.open_tab(filename)
        dialog.destroy()

    def open_tab(self, filename):
        img = Image.open(filename)
        pixbuf = self.create_pixbuf(img)
        img_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        pos = filename.rfind('/')
        filename = filename[pos+1:]
        self.images.append([img, filename])
        self.create_tab(img_widget, filename)

    def create_tab(self, img_widget=None, title='Sans-titre'):
        """Create a tab containing the picture.

        Connect the mouse wheel for zoom.
        Disable scrolling the scrolledindow with mouse wheel.
        Use TabLabel and connect it to close the tab.

        :param img_widget: image widget created by create_pixbuf
        :param: title: title of the picture: filename

        """
        page = Gtk.Box()
        page.set_hexpand(True)  # Fill available horizontal space
        page.set_vexpand(True)  # Fill available vertical space
        scrolled_window = Gtk.ScrolledWindow()
        #scrolled_window.set_overlay_scrolling(True)
        page.pack_start(scrolled_window, True, True, 0)
        if img_widget is not None:
            scrolled_window.add(img_widget)
        tab_label = TabLabel(title)
        tab_label.connect('close-clicked', self.on_close_clicked, page)
        self.notebook.append_page(page, tab_label)
        #self.notebook.set_tab_reorderable(page, True)
        self.notebook.show_all()

    def create_pixbuf(self, img, ext='jpeg'):
        """Convert a PIL image to Gtk pixbuf.

        :param img : PIL image

        """
        buff = BytesIO()
        img.save(buff, ext)
        content = buff.getvalue()
        buff.close()
        loader = GdkPixbuf.PixbufLoader()
        loader.write(content)
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf

    def on_close_clicked(self, _, page):
        """Close a tab."""
        index = self.notebook.page_num(page)
        self.close_tab(index)

    def close_tab(self, index):
        self.notebook.remove_page(index)
        self.images.pop(index)

    def filter(self, func):
        page = self.notebook.get_current_page()
        self.images[page][0] = func(self.images[page][0])
        pixbuf = self.create_pixbuf(self.images[page][0])
        new_img_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        box = self.notebook.get_nth_page(page)
        scrolled_window = box.get_children()[0]
        scrolled_window.remove(scrolled_window.get_children()[0])  # Remove old image
        scrolled_window.add(new_img_widget)
        self.notebook.show_all()

    def file_save(self, action):
        index = self.notebook.get_current_page()
        self.images[index][0].save(self.images[index][1])

    def file_save_as(self, action):
        index = self.notebook.get_current_page()

        dialog = Gtk.FileChooserDialog('Choisissez un fichier', self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.images[index][0].save(filename)
            self.close_tab(index)
            self.open_tab(filename)

        dialog.destroy()

    def about(self, action):
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
