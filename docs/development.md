# Development Info

- [Overview](#overview)
- [Contributing](#contributing)
  - [Issues](#issues)
  - [Pull requests](#pull-requests)
- [Upcoming features](#upcoming-features)

## Overview

xinput-gui is written in Python 3. The GUI uses GTK+ 3 and was made using the Glade interface designer.

Internally, xinput-gui wraps around the `xinput` command by calling it and parsing it's output.

## Contributing

### Issues

Please feel free to open issues with bugs, feature requests, or any other discussion you find necessary.

If you're reporting a bug, remember to include your version of xinput-gui (can be found in `Help -> About`), your operating system version, detailed steps to reproduce the bug, and, if it helps, a screenshot.

### Pull requests

Pull requests are always welcome, but before you start working on a feature/bugfix, *open an issue*. Pull requests that haven't been discussed beforehand may take a while to merge, or not be merged at all. Before you start putting work into a feature, open an issue for discussion to make sure that it's something that's wanted by the project.

## Upcoming features

This is a rough roadmap of planned features:

- Log all commands and their output
  - This allows for better error handling
- Save and display a list of all changes, and allow them to be easily copied and pasted into an Xorg config file to make them persistent
- Allow testing devices
- Button mapping
- Move away from parsing `xinput` command
  - Move directly to X11 APIs
  - Use libinput
  - Both of these approaches could add more complexity than desired
