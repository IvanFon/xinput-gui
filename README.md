# xinput-gui
A simple GUI for Xorg's Xinput tool.

| ![](https://user-images.githubusercontent.com/1174413/61573693-78d29000-aaa2-11e9-834c-2d7f35c765e3.png) | ![](https://user-images.githubusercontent.com/1174413/61573694-78d29000-aaa2-11e9-902f-7c5989cc43f8.png) |
| --- | --- |

xinput allows you to edit properties of devices like keyboards, mice, and touchpads. This GUI wraps around the xinput command to make editing them faster and more user-friendly.

<img align="right" src="https://user-images.githubusercontent.com/1174413/61573695-78d29000-aaa2-11e9-80ee-7dc2e19d31e8.png" width="400px">

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

Clone this repo and run `./setup.py install --user`.

## Usage

Just run `xinput-gui`. Selecting a device will list all of it's properties. When editing them, changes will be applied immediately.

## Contributing

xinput-gui is written in Python 3. The GUI uses GTK+ 3 and was made using the Glade interface designer.

Please feel free to open issues with bugs, feature requests, or any other discussion you find necessary.

Pull requests are always welcome, but please make sure that there's an open issue for the bug you're fixing/feature you're adding first. Pull requests that are submitted that haven't already been discussed likely won't be or will take a while to be accepted. This is the kind of tool that can easily become bloated/difficult to use/get out of scope, so I do want to be fairly careful about what features are added.


<3
