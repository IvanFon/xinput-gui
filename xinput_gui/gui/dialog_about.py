# dialog_about.py - about dialog
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

'''About dialog.'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import require, resource_filename


__version__ = require('xinput_gui')[0].version


class AboutDialog:
    '''About dialog.'''

    def __init__(self, main_window) -> None:
        '''Init AboutDialog.'''

        builder = self.get_builder()

        builder.connect_signals(AboutDialog.SignalHandler(self))

        self.dialog_about = builder.get_object('dialog_about')

        self.dialog_about.set_version(__version__)
        self.dialog_about.set_transient_for(main_window.win_main)

    def get_builder(self) -> Gtk.Builder:
        '''Get about dialog Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['dialog_about'])
        return builder

    def show(self) -> None:
        '''Show the about dialog.'''

        self.dialog_about.run()

    class SignalHandler:
        '''Handle about dialog signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_dialog_about_response(self, *args) -> None:
            '''dialog_about "response" signal.'''

            self.gui.dialog_about.hide()
