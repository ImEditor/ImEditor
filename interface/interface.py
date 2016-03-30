#!/usr/bin/python3

from gi.repository import Gtk, Gdk, GdkPixbuf
from PIL import Image
from os import path

from interface.tabs import TabLabel
from interface.menus import create_menus
from interface.dialog import dialog_param, dialog_new_image
from interface.tools import create_pixbuf, about

def img_open(func_):
    """Need open image."""
    # func_ is the decorated function
    # func is the method to apply
    def inner(self, func, value=None):
        if len(self.images) > 0:
            if value is None:
                return func_(self, func)
            else:
                return func_(self, func, value)
    return inner

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
        self.MAX_HIST = 10

    def quit_app(self, *args):
        Gtk.main_quit()

    def open_image(self, *args):
        dialog = Gtk.FileChooserDialog('Choisissez un fichier',
            self,
            Gtk.FileChooserAction.OPEN,
            ("Annuler", Gtk.ResponseType.CANCEL,
             "Ouvrir", Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.open_tab(filename)
        dialog.destroy()

    def new_image(self, size, color='red'):
        img = Image.new('RGB', size, color)
        pixbuf = create_pixbuf(img)
        img_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        self.images.append([[img], 'noname.jpg', 0])
        self.create_tab(img_widget)

    def open_tab(self, filename):
        img = Image.open(filename)
        pos = filename.find('.')

        pixbuf = create_pixbuf(img)
        img_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        pos = filename.rfind('/')
        basename = filename[pos+1:]
        self.images.append([[img], filename, 0])
        self.create_tab(img_widget, basename)

    def create_tab(self, img_widget=None, title='Sans-titre'):
        """Create a tab containing the picture.

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

    def on_close_clicked(self, _, page):
        """Close a tab."""
        index = self.notebook.page_num(page)
        self.close_tab(index)

    def close_tab(self, index):
        self.notebook.remove_page(index)
        self.images = self.images[:index] + self.images[index+1:]
        # add close img from PIL

    @img_open
    def filter(self, func, value=None):
        print('filter')
        print(self.images)
        page = self.notebook.get_current_page()
        index_img = self.images[page][2]
        if value is None:
            new_img = func(self.images[page][0][index_img])
        else:
            new_img = func(self.images[page][0][index_img], value)
        self.edit_image(new_img, page)
        self.images[page][0] = self.images[page][0][:index_img+1]
        print(self.images)
        self.images[page][0].append(new_img)
        self.images[page][2] += 1
        if len(self.images[page][0]) > self.MAX_HIST:
            print('ok')
            self.images[page][0].pop(0)
            self.images[page][2] -= 1
        print(self.images)

        print('filter /')

    def edit_image(self, new_img, page):
        """Manage editing image.

        Show new image.
        """

        # Show image:
        pixbuf = create_pixbuf(new_img)
        new_img_widget = Gtk.Image.new_from_pixbuf(pixbuf)
        box = self.notebook.get_nth_page(page)
        scrolled_window = box.get_children()[0]
        scrolled_window.remove(scrolled_window.get_children()[0])  # Remove old image
        scrolled_window.add(new_img_widget)
        self.notebook.show_all()

    @img_open
    def history(self, num):
        print('history')
        print(self.images)
        page = self.notebook.get_current_page()
        if len(self.images[page][0]) >= 2:
            print('ok')
            index_img = self.images[page][2]

            if num == -1: # Undo:
                if index_img >= 1:
                    self.images[page][2] += num
                    index_img = self.images[page][2]
                    self.edit_image(self.images[page][0][index_img], page)
            else: # Redo:
                if index_img + 1 < len(self.images[page][0]):
                    self.images[page][2] += num
                    index_img = self.images[page][2]
                    self.edit_image(self.images[page][0][index_img], page)

        print(self.images)
        print('history /')

    @img_open
    def properties(self, action):
        page = self.notebook.get_current_page()
        index_img = self.images[page][2]
        img = self.images[page][0][index_img]

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, 'Propriétés de l\'image')
        message = '<b>Taille : </b>' + str(img.width) + 'x' + str(img.height) + ' <b>Mode : </b>' + img.mode
        dialog.format_secondary_markup(message)
        dialog.run()

        dialog.destroy()

    @img_open
    def file_save(self, action):
        print(action)
        page = self.notebook.get_current_page()
        index_img = self.images[page][2]
        self.images[page][0][index_img].save(self.images[page][1])

    @img_open
    def file_save_as(self, action):
        page = self.notebook.get_current_page()

        dialog = Gtk.FileChooserDialog('Choisissez un fichier', self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            index_img = self.images[page][2]
            self.images[page][0][index_img].save(filename)
            self.close_tab(page)
            self.open_tab(filename)

        dialog.destroy()

    def filter_with_params(self, func, title, limits):
        dialog_param(func, self, title, limits)

    def about(self, action):
        about()
