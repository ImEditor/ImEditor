# ImEditor

[![Requirements Status](https://requires.io/github/ImEditor/ImEditor/requirements.svg?branch=master)](https://requires.io/github/ImEditor/ImEditor/requirements/?branch=master)
[![Snap Status](https://build.snapcraft.io/badge/ImEditor/ImEditor.svg)](https://build.snapcraft.io/user/ImEditor/ImEditor)

ImEditor is a simple & versatile image editor.

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

## Installation instructions

### Universal package for Linux (recommended)

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/imeditor)

    snap install imeditor

### Build from source

Build and install by running:

    python setup.py build
    sudo python setup.py install

### Developer install

Installing ImEditor with develop mode creates binaries that link back to source code. Therefore changes will be reflected immediately with no need to repeatedly install.

    sudo python setup.py develop

## Tech

ImEditor uses a number of open source projects to work properly:

- [GTK 3](https://www.gtk.org)
- [Python 3](https://www.python.org)
- [Pillow](https://python-pillow.org)

## License

GNU GENERAL PUBLIC LICENSE (v3)

**Free Software, Hell Yeah!**
