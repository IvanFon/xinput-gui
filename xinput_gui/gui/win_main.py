# win_main.py - main app window
# Copyright (C) 2019  Ivan Fonseca
#
# This file is part of xinput-gui.
#
# xinput-gui is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the # License,
# or (at your option) any later version.
#
# xinput-gui is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with xinput-gui.  If not, see <https://www.gnu.org/licenses/>.

'''Main app window.'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import require, resource_filename

from ..settings import Settings
from ..xinput.xinput import Xinput
from .device_list import DeviceList
from .dialog_about import AboutDialog
from .prop_list import PropList
from .win_settings import SettingsWindow


__version__ = require('xinput_gui')[0].version


class MainWindow:
    '''Main app window.'''

    def __init__(self, settings: Settings, xinput: Xinput) -> None:
        '''Init MainWindow.'''

        self.settings = settings
        self.xinput = xinput
        self.refreshing = False

        builder = self.get_builder()

        builder.connect_signals(MainWindow.SignalHandler(self))

        self.win_main = builder.get_object('win_main')
        self.box_main = builder.get_object('box_main')

        self.win_main.set_title('Xinput GUI {}'.format(__version__))
        self.win_main.show_all()

        self.device_list = DeviceList(self, settings, xinput)
        self.prop_list = PropList(self, settings, xinput)
        self.about_dialog = AboutDialog(self)
        self.settings_window = SettingsWindow(self, settings)

        self.box_main.pack_start(self.device_list.grid_device_list,
                                 True, True, 0)
        self.box_main.pack_start(self.prop_list.grid_prop_list,
                                 True, True, 0)

        self.apply_settings()

        Gtk.main()

    def get_builder(self) -> Gtk.Builder:
        '''Get main window Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['win_main'])
        return builder

    def apply_settings(self) -> None:
        '''Apply current settings.'''

        self.device_list.apply_settings()
        self.prop_list.apply_settings()

        # Vertical layout
        if self.settings.vertical_layout:
            self.box_main.set_orientation(Gtk.Orientation.VERTICAL)
            self.win_main.resize(600, 600)
        else:
            self.box_main.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.win_main.resize(800, 400)

    def show_settings_window(self) -> None:
        '''Shows the settings window.'''

        self.settings_window.show()

    def show_about_dialog(self) -> None:
        '''Shows the about dialog.'''

        self.about_dialog.show()

    class SignalHandler:
        '''Handle main window signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_win_main_destroy(self, *args) -> None:
            '''win_main "destroy" signal.'''

            Gtk.main_quit()

        def on_menu_settings_activate(self, *args) -> None:
            '''menu_settings "activate" signal.'''

            self.gui.show_settings_window()

        def on_menu_about_activate(self, *args) -> None:
            '''menu_about "activate" signal.'''

            self.gui.show_about_dialog()
