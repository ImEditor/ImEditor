# ImEditor

## Simple & versatile image editor.

[![Requirements Status](https://requires.io/github/ImEditor/ImEditor/requirements.svg?branch=master)](https://requires.io/github/ImEditor/ImEditor/requirements/?branch=master)

ImEditor is a simple image editor, supporting PNG, JPEG, WEBP, BMP, and ICO file types.
It offers several tools to easily modify an image.

### Functionalities

- Tabs
- Create or open an image
- Drawing capacities
- Apply filters on an image
- History feature
- Copy/paste/cut features
- Selection feature
- Few basic operations (rotate, image details,…)

### Supported formats

PNG, JPEG, WEBP, BMP, ICO

### Supported modes

RGB, RGBA

## Screenshot

![ImEditor](data/screenshots/screen1.png)

## Installation instructions

### Universal package for Linux (recommended)
    
A flatpak package will be available soon :

https://github.com/flathub/flathub/pull/1089

### Build from source (nightly)

Build and install by running:

    git clone https://github.com/ImEditor/ImEditor.git
    cd ImEditor
    meson _build
    cd _build
    ninja
    sudo ninja install

The app can then be removed with:

    sudo ninja uninstall

## Tech

ImEditor uses a number of open source projects to work properly:

- [GTK 3](https://www.gtk.org)
- [Python 3](https://www.python.org)
- [Pillow](https://python-pillow.org)

## License

GNU GENERAL PUBLIC LICENSE (v3)

**Free Software, Hell Yeah!**
