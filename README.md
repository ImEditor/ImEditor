# ImEditor

## Simple & versatile image editor.

[![Requirements Status](https://requires.io/github/ImEditor/ImEditor/requirements.svg?branch=master)](https://requires.io/github/ImEditor/ImEditor/requirements/?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/0b9e7af147bd50c8f76d/maintainability)](https://codeclimate.com/github/ImEditor/ImEditor/maintainability)

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

ImEditor is available as a flatpak package.

<a href='https://flathub.org/apps/details/io.github.ImEditor'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>

You can also install it by using the following command-line:

    flatpak install flathub io.github.ImEditor

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
