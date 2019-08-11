# view_controller.py - app view controller
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

'''App view controller.'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .gui.win_main import MainWindow
from .settings import Settings
from .xinput.xinput import Xinput


class ViewController:
    '''App view controller.'''

    def __init__(self) -> None:
        '''Init ViewController.'''

        self.settings = Settings()
        self.xinput = Xinput()
        self.main_window = MainWindow(self.settings, self.xinput)
        self.device_list = self.main_window.device_list
        self.prop_list = self.main_window.prop_list
        self.log = self.main_window.log

        self.xinput.set_controller(self)

        self.device_list.refresh_devices()

    def start(self) -> None:
        '''Start app.'''

        Gtk.main()

    def log_updated(self) -> None:
        '''Xinput log updated.'''

        self.log.update()
