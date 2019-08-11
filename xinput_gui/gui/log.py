# log.py - log
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

'''Log.'''

from typing import TYPE_CHECKING

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..xinput.xinput import Xinput

if TYPE_CHECKING:
    from .win_main import MainWindow


class Log:
    '''Log.'''

    def __init__(self, main_window: 'MainWindow', xinput: Xinput):
        '''Init Log.'''

        self.main_window = main_window
        self.xinput = xinput

        builder = self.get_builder()

        builder.connect_signals(Log.SignalHandler(self))

        self.grid_log = builder.get_object('grid_log')
        self.buffer_log = builder.get_object('buffer_log')
        self.text_log = builder.get_object('text_log')
        self.btn_clear_log = builder.get_object('btn_clear_log')

    def get_builder(self) -> Gtk.Builder:
        '''Get device list Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['grid_log', 'buffer_log'])
        return builder

    def clear_log(self) -> None:
        '''Clear the log.'''

        self.buffer_log.set_text('')

        # Unfocus clear button
        self.main_window.win_main.set_focus(None)

    def update(self) -> None:
        '''Update log.'''

        self.buffer_log.set_text(self.xinput.log)

    class SignalHandler:
        '''Handle log signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_btn_clear_log_clicked(self, *args) -> None:
            '''btn_clear_log "clicked" signal.'''

            self.gui.clear_log()
