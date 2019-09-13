import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib

from .window import ImEditorWindow


APP_ID = 'io.github.ImEditor'


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID,
                        flags=Gio.ApplicationFlags.HANDLES_OPEN)
        self.win = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        GLib.set_application_name('ImEditor')
        GLib.set_prgname(APP_ID)

        self.connect('open', self.file_open_handler)

    def do_activate(self):
        if not self.win:
            self.win = ImEditorWindow(application=self)
        self.win.present()

    def file_open_handler(self, app, g_file_list, amount, ukwn):
        for g_file in g_file_list:
            self.win.open_image(filename=g_file.get_path())

        self.do_activate()


def main(version):
    app = Application()
    return app.run(sys.argv)
