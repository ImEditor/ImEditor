# -*- coding: utf-8 -*-
#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf
from PIL import Image

from interface import tools

class Vars(object):
	"""Base class"""
	def setup_method(self, _):
		self.img = Image.new('RGB', (1, 1))

class TestTools(Vars):
    def test_pil_to_pixbuf(self):
        assert type(tools.pil_to_pixbuf(self.img)) == GdkPixbuf.Pixbuf
