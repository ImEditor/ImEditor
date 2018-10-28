# Change Log
All notable changes to this project will be documented in this file.

## [0.7] - DEV
### Added
- Allow copy/paste things betweens tabs.
- Permit to handle zoom with the ctrl key + mouse wheel.
- Make tabs reordable.

### Changed
- Prefer a dark theme if available.
- Better adjust the zoom level when an image is opened.
- Open the color selector directly when choosing a custom background color.

### Fixed
- Make icons of the header bar visbile even with a dark background.
- Change window's title if an image have changed of name during saving.

## [0.6.2] - 2017-12-29
### Fixed
- Finally fix the closing bug (really ...).

## [0.6.1] - 2017-12-29
### Fixed
- Fix the bug that caused the wrong tab to close.

## [0.6] - 2017-12-27
### Added
- Allow to open files in ImEditor from your favorite file manager.
- Allow to open files by using the command line.
- Make the opened image fit the window.
- Add rotate functions also in the "operations" submenu.

### Fixed
- Remove duplicated "cut" entry from the menu.
- Make undo/redo rework for crop and rotate functions.

## [0.5.2] - 2017-12-23
### Changed
- Improve way to launch the app.

## [0.5.1] - 2017-12-23
### Fixed
- Improve the PKGBUILD and use standard folders to store the app.

## [0.5] - 2017-12-22
### Changed
- Preserve ratio of the image in the preview icon.
- Compress images used by the app.
- Add a bottom margin to the homescreen.
- Only allow the left mouse button to do actions.

### Fixed
- Fix copying of entire image when selecting a 0px area.
- Fix the problem of the crappy display when zooming.
- Fix cropping and copying when not starting selection by the top-left corner.

## [0.4] - 2017-12-09
### Added
- Add zoom feature.

### Changed
- Rework a few things in details dialog.
- Improve behavior of copy/paste/cut actions.

### Fixed
- Fix behavior of tools buttons when switching tab.
- Various optimizations.

## [0.3] - 2017-11-30
### Added
- Add crop feature.

### Changed
- Higher limit for the history (20 to 100).

### Fixed
- Don't permit to open several times the same image.
- Don't call the close_tab function two times when closing a tab.
- Disable mirror actions when any image is open.
- Various optimizations.

## [0.2] - 2017-11-27
### Added
- Add a new submenu "Operations".
- Add horizontal and vertical mirror features.
- Add 1024x768, 1280x1024, 1920x1200 in template list.
- Ctrl+W can be used to close a tab.

### Changed
- Only support RGB and RGBA images to not alter the format of the original images.
- Improve way to choose background color when creating a new image.

### Fixed
- Finally fix the high-ram usage !!!
- Various optimizations.

## [0.1.1] - 2017-11-11
### Fixed
- Fix rotate feature.

## [0.1] - 2017-11-11
- First alpha.
