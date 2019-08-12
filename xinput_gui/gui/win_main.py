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

from typing import TYPE_CHECKING

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import require, resource_filename

from ..settings import Settings
from .device_list import DeviceList
from .dialog_about import AboutDialog
from .log import Log
from .prop_list import PropList
from .win_settings import SettingsWindow

if TYPE_CHECKING:
    from ..view_controller import ViewController


__version__ = require('xinput_gui')[0].version


class MainWindow:
    '''Main app window.'''

    def __init__(self, controller: 'ViewController', settings: Settings) -> None:
        '''Init MainWindow.'''

        self.controller = controller
        self.settings = settings
        self.refreshing = False

        builder = self.get_builder()

        builder.connect_signals(MainWindow.SignalHandler(self))

        self.win_main = builder.get_object('win_main')
        self.box_editor = builder.get_object('box_stack_editor')
        self.box_log = builder.get_object('box_stack_log')

        self.win_main.set_title('Xinput GUI {}'.format(__version__))
        self.win_main.show_all()

        self.about_dialog = AboutDialog(self)
        self.device_list = DeviceList(controller, self, settings)
        self.log = Log(self)
        self.prop_list = PropList(controller, self, settings)
        self.settings_window = SettingsWindow(self, settings)

        self.box_editor.pack_start(self.device_list.grid_device_list,
                                 True, True, 0)
        self.box_editor.pack_start(self.prop_list.grid_prop_list,
                                 True, True, 0)

        self.box_log.pack_start(self.log.grid_log, True, True, 0)

        self.apply_settings()

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
            self.box_editor.set_orientation(Gtk.Orientation.VERTICAL)
            self.win_main.resize(600, 800)
        else:
            self.box_editor.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.win_main.resize(900, 450)

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
