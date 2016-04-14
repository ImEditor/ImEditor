# -*- coding: utf-8 -*-
#!/usr/bin/python3

def get_coords(img_size, tab_size, pos_mouse):
    top_space = (tab_size.height - img_size.height) / 2
    left_space = (tab_size.width - img_size.width) / 2
    if top_space > 0:
        y = round(pos_mouse.y - top_space)
    else:
        y = round(pos_mouse.y)
    if left_space > 0:
        x = round(pos_mouse.x - left_space)
    else:
        x = round(pos_mouse.x)
    return x, y
