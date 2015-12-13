#!/usr/bin/python3

from gi.repository import Gtk, Gdk
from gi.repository import GdkPixbuf
import sys
from PIL import Image
import io

from interface.tabs import TabLabel

class App(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='ImEditor')
        self.set_default_size(700, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('delete-event', Gtk.main_quit)

        grid = Gtk.Grid()
        self.add(grid)

        # Menu:
        action_group = Gtk.ActionGroup('my_actions')
        action_group.add_actions([
            ('FileMenu', None, 'Fichier'),
            ('FileOpen', Gtk.STOCK_OPEN, None, '<control>O', None, self.open_file),
            ('EditMenu', None, 'Edit'),
            ('EditCopy', Gtk.STOCK_COPY, None, '<control>C', None, None)
        ])
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_file('menubar.ui')
        # accelerator ?
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget("/MenuBar")
        grid.add(menubar)

        # Tabs:
        self.notebook = Gtk.Notebook()
        grid.add(self.notebook)

    def open_file(self, _):
        dialog = Gtk.FileChooserDialog('Choisissez un fichier', self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            image = Image.open(filename)
            pos = filename.rfind('/')
            self.show_image(image, filename[pos+1:])
        dialog.destroy()

    def show_image(self, image, title='Sans-titre'):
        """Create new tab loading image."""
        page = Gtk.Box()
        pixbuf = self.create_pixbuf(image)
        image_wid = Gtk.Image.new_from_pixbuf(pixbuf)
        page.add(image_wid)
        tab_label = TabLabel(title)
        tab_label.connect('close-clicked', self.on_close_clicked, page)
        self.notebook.append_page(page, tab_label)
        self.notebook.show_all()

    def on_close_clicked(self, _, page):
        self.notebook.remove_page(self.notebook.page_num(page))


    def create_pixbuf(self, im, ext='jpeg'):
        """Convert PIL image to Gtk pixbuf."""
        buff = io.BytesIO()
        im.save(buff, ext)
        content = buff.getvalue()
        buff.close()
        loader = GdkPixbuf.PixbufLoader()
        loader.write(content)
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf

if __name__ == '__main__':
    app = App()
    app.show_all()
    Gtk.main()
