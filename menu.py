from gi.repository import Gtk

class MenuExampleWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Menu Example")
        self.set_default_size(200, 200)

        action_group = Gtk.ActionGroup("my_actions")

        # file:
        # 1 arg: name of object in .ui :
        # 2nd arg: label
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenewmenu = Gtk.Action("FileOpen", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenewmenu)
        # edit:
        action_group.add_actions([
            ("EditMenu", None, "Edit"),
            ("EditCopy", Gtk.STOCK_COPY, None, "<control>C", None, None)
        ])

        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_file('menubar.ui')
        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)

        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)
        self.add(box)


window = MenuExampleWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
