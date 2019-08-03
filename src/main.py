import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio

from .window import ImEditorWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='io.github.ImEditor',
                        flags=Gio.ApplicationFlags.HANDLES_OPEN)

        self.connect('activate', self.show_window)
        self.connect('open', self.open_files)
        self.win = None

    def show_window(self, *args):
        self.win = self.props.active_window
        if not self.win:
            self.win = ImEditorWindow(application=self)
        self.win.present()

    def open_files(self, app, files, hint, *args):
        self.show_window()
        for image in files:
            self.win.open_image(filename=image)


def main(version):
    app = Application()
    return app.run(sys.argv)
