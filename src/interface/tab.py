import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from os import path

from .editor import Editor
from .tools import create_empty_pixbuf, pil_to_pixbuf, SpinButton


class Tab(Gtk.Box):
    def __init__(self, win, img, filename, saved):
        Gtk.Box.__init__(self)
        self.win = win
        self.editor = Editor(self, img, filename, saved)

        # Image
        pixbuf = create_empty_pixbuf(img)
        self.img_widget = Gtk.Image.new_from_pixbuf(pixbuf)

        event_box = Gtk.EventBox()
        event_box.connect('button-press-event', self.editor.handle_event, 'press')
        event_box.connect('motion-notify-event', self.editor.handle_event, 'move')
        event_box.connect('button-release-event', self.editor.handle_event, 'release')
        event_box.add(self.img_widget)

        frame = Gtk.Frame(hexpand=True, vexpand=True)
        frame.set_halign(Gtk.Align.CENTER)
        frame.set_valign(Gtk.Align.CENTER)
        frame.set_name('TabFrame')
        frame.add(event_box)
        css = b"""#TabFrame {
          background-image: linear-gradient(45deg, #808080 25%, transparent 25%), linear-gradient(-45deg, #808080 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #808080 75%), linear-gradient(-45deg, transparent 75%, #808080 75%);
          background-size: 20px 20px;
          background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
        }"""
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.connect('scroll-event', self.scroll_zoom)
        scrolled_window.add(frame)

        # Sidebar
        self.sidebar_frame = Gtk.Frame()

        # Pencil
        self.pencil_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
            border_width=25, spacing=10)
        pencil_label = Gtk.Label('<b>' + _("Pencil") + '</b>', use_markup=True)
        shape_pencil_label = Gtk.Label(_("Shape"))
        pencil_shape_combo = Gtk.ComboBoxText()
        pencil_shape_combo.set_entry_text_column(0)
        shapes = [_("Ellipse"), _("Square")]
        for shape in shapes:
            pencil_shape_combo.append_text(shape)
        pencil_shape_combo.set_active(0)
        pencil_shape_combo.connect('changed', self.on_pencil_shape_changed)
        color_pencil_label = Gtk.Label(_("Color"))
        pencil_color_button = Gtk.ColorButton()
        pencil_color_button.set_use_alpha(False)
        pencil_color_button.set_rgba(Gdk.RGBA(0, 0, 0, 1))
        pencil_color_button.connect('color-set', self.on_pencil_color_changed)
        size_pencil_label = Gtk.Label('Size')
        pencil_size_spin = SpinButton(8, 1, 1000, 1, 2)
        pencil_size_spin.connect('value-changed', self.on_pencil_size_changed)
        self.pencil_box.add(pencil_label)
        self.pencil_box.add(shape_pencil_label)
        self.pencil_box.add(pencil_shape_combo)
        self.pencil_box.add(color_pencil_label)
        self.pencil_box.add(pencil_color_button)
        self.pencil_box.add(size_pencil_label)
        self.pencil_box.add(pencil_size_spin)

        self.sidebar_frame.add(self.pencil_box)

        # Main Box
        self.add(scrolled_window)
        self.add(self.sidebar_frame)

        self.tab_label = TabLabel(win, self, path.basename(filename), img)

        # Vars
        self.width = self.disp_width = img.width
        self.height = self.disp_height = img.height
        self.zoom_level = self.best_zoom_level()
        self.last_pixbuf = pixbuf

        # Initialize image
        self.update_image(img)
        self.set_zoom_level()

        self.show_all()
        self.pencil_box.hide()
        self.enable_sidebar(False)

    def update_image(self, img=None, tmp=False):
        """Refresh the displayed image"""
        if img:
            self.editor.image.size = img.size  # in case it changed
        # Vars
        width, height = self.editor.image.size
        # Create pixbuf
        pixbuf = pil_to_pixbuf(img) if img else self.last_pixbuf
        # Update preview and save pixbuf if it's not a temp change
        if not tmp:
            self.tab_label.set_icon(pixbuf)
            self.last_pixbuf = pixbuf
        # Update the image and the icon
        if self.zoom_level != 100:
            # Change displaying size
            width *= self.zoom_level / 100
            height *= self.zoom_level / 100
        pixbuf = pixbuf.scale_simple(width, height,
            GdkPixbuf.InterpType.BILINEAR)
        self.img_widget.set_from_pixbuf(pixbuf)
        self.disp_width, self.disp_height = width, height

    def enable_sidebar(self, enable=True):
        """Show or hide the sidebar"""
        if enable:
            self.sidebar_frame.show()
            if self.editor.task == 2:
                self.pencil_box.show()
        else:
            self.sidebar_frame.hide()

    def zoom(self, value):
        """Change the zoom value"""
        self.zoom_level += value * 10
        self.zoom_level = round(self.zoom_level / 10) * 10  # round to the nearest decade
        # Limit zoom between 10-300%
        if self.zoom_level < 10:
            self.zoom_level = 10
        elif self.zoom_level > 300:
            self.zoom_level = 300
        self.set_zoom_level()

    def scroll_zoom(self, widget, event):
        """Handle zoom with scroll wheel"""
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            is_smooth, dx, dy = Gdk.Event.get_scroll_deltas(event)
            if is_smooth:
                if dy > 0:
                    self.zoom(-1)
                elif dy < 0:
                    self.zoom(1)
            elif event.direction == Gdk.ScrollDirection.UP:
                self.zoom(1)
            elif event.direction == Gdk.ScrollDirection.DOWN:
                self.zoom(-1)

    def best_zoom_level(self):
        """Find the best zoom level at start"""
        zoom = 100  # default zoom
        w, h = self.editor.image.size  # size of the image
        ww = self.win.get_allocation().width  # width of the window
        wh = self.win.get_allocation().height  # height of the window
        ww -= ww * 35 / 100  # add a margin
        wh -= wh * 35 / 100  # add a margin
        # If the image is higher than the window
        if w > ww or h > wh:
            # Calculate the ratio image/window
            ratio_w = w / ww
            ratio_h = h / wh
            ratio = round(max((ratio_w, ratio_h)), 1)

            zoom = int(round(zoom / ratio))

            w = int(zoom * w / 100)
            h = int(zoom * h / 100)
        return zoom

    def set_zoom_level(self):
        """Make the zoom level change"""
        self.update_image(tmp=True)
        self.win.set_window_title(self)

    def on_pencil_shape_changed(self, button):
        shape = button.get_active_text()
        if shape == _("Ellipse"):
            self.editor.pencil_shape = 0
        elif shape == _("Square"):
            self.editor.pencil_shape = 1

    def on_pencil_color_changed(self, button):
        self.editor.pencil_color = button.get_rgba().to_string()

    def on_pencil_size_changed(self, button):
        self.editor.pencil_size = button.get_value_as_int()


class TabLabel(Gtk.Box):
    """Define the label of the tab."""
    def __init__(self, win, tab, title, img):
        Gtk.Box.__init__(self)
        self.set_spacing(5)

        self.win = win
        self.tab = tab

        # Preview of image
        self.icon = Gtk.Image()

        # Title
        self.label = Gtk.Label()
        self.set_title(title)

        # Close button
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.add(Gtk.Image.new_from_icon_name('window-close',
            Gtk.IconSize.MENU))
        button.connect('clicked', self.on_close_button_clicked)
        self.add(self.icon)
        self.add(self.label)
        self.add(button)

        self.show_all()

    def on_close_button_clicked(self, _):
        page_num = self.win.notebook.page_num(self.tab)
        self.win.close_tab(page_num=page_num)

    def set_title(self, title):
        """Change the title of a tab"""
        max_size = 30  # limit the length of the title
        if len(title) > max_size:
            title = title[:max_size - 3] + "..."
        self.label.set_text(title)

    def set_icon(self, pixbuf):
        """Change the preview icon"""
        # Find height and width to preserve ration of the image in the icon
        width, height = pixbuf.get_width(), pixbuf.get_height()
        if width > height:
            icon_width = 24
            icon_height = icon_width * height / width
        else:
            icon_height = 24
            icon_width =  icon_height * width / height
        pixbuf = pixbuf.scale_simple(icon_width, icon_height,
            GdkPixbuf.InterpType.TILES)
        self.icon.set_from_pixbuf(pixbuf)
