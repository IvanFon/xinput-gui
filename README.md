# xinput-gui
A simple GUI for Xorg's Xinput tool.

| ![](https://user-images.githubusercontent.com/1174413/61573693-78d29000-aaa2-11e9-834c-2d7f35c765e3.png) | ![](https://user-images.githubusercontent.com/1174413/61573694-78d29000-aaa2-11e9-902f-7c5989cc43f8.png) |
| --- | --- |

xinput allows you to edit properties of devices like keyboards, mice, and touchpads. This GUI wraps around the xinput command to make editing them faster and more user-friendly.

## Installation

xinput-gui depends on Python 3.5+, GTK+ 3.20+, PyGObject, and xinput.

### Arch Linux

Available as a package on the AUR: [xinput-gui](https://aur.archlinux.org/packages/xinput-gui)

Install it with `makepkg` or your preferred AUR helper.

### Gentoo

Available as a Gentoo package thanks to [@filalex77](https://github.com/filalex77): [app-misc/xinput-gui](https://github.com/filalex77/bright/tree/master/app-misc/xinput-gui)

To install it, run the following commands:

```
eselect-repository enable bright
emerge --sync
emerge xinput-gui
```

### pip

Available on PyPI: [xinput-gui](https://pypi.org/project/xinput-gui/)

Install it with pip: `pip install --user xinput-gui`.

### Manual install

Download the [latest release](https://github.com/IvanFon/xinput-gui/releases/latest) or clone this repo and run `./setup.py install --user`.

## Usage

Just run `xinput-gui`. Selecting a device will list all of it's properties. When editing them, changes will be applied immediately.

For detailed usage instructions, information on development and contributing, and more, see the [documentation](docs/overview.md).
