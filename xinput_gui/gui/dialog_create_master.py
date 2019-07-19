# dialog_create_master.py - create master device dialog
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

'''Create master device dialog.'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..xinput.xinput import Xinput


class CreateMasterDialog:
    '''Create master device dialog.'''

    def __init__(self, main_window, xinput: Xinput) -> None:
        '''Init CreateMasterDialog.'''

        self.main_window = main_window
        self.xinput = xinput

        builder = self.get_builder()

        builder.connect_signals(CreateMasterDialog.SignalHandler(self))

        self.dialog_create_master = builder.get_object('dialog_create_master')
        self.entry_new_master_name = builder.get_object('entry_new_master_name')
        self.btn_create = builder.get_object('btn_create_master_create')

        self.dialog_create_master.set_transient_for(main_window.win_main)

    def get_builder(self) -> Gtk.Builder:
        '''Get create master device dialog Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['dialog_create_master'])
        return builder

    def show(self) -> None:
        '''Show the create master device dialog.'''

        # Setup dialog

        self.entry_new_master_name.set_text('')
        self.entry_new_master_name.grab_focus()
        # Default error message
        self.check_errors()

        # Show dialog

        res = self.dialog_create_master.run()
        if res == Gtk.ResponseType.APPLY:
            new_master_name = self.entry_new_master_name.get_text()

            self.xinput.create_master_device(new_master_name)
            self.main_window.refresh_devices()

        self.dialog_create_master.hide()

    def change_error_message(self, message: str) -> None:
        '''Change the error message label.'''

        self.dialog_create_master.get_message_area().get_children()[1].set_label(message)

    def check_errors(self) -> None:
        '''Check for errors in the new device name.'''

        name = self.entry_new_master_name.get_text()

        self.btn_create.set_sensitive(False)

        if name == '':
            self.change_error_message('Error: device name cannot be blank.')
            return

        self.change_error_message('Device name valid.')
        self.btn_create.set_sensitive(True)

    class SignalHandler:
        '''Handle create master device dialog signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_entry_new_master_name_activate(self, *args) -> None:
            '''entry_new_master_name "activate" signal.'''

            self.gui.btn_create.clicked()

        def on_entry_new_master_name_changed(self, *args) -> None:
            '''entry_new_master_name "changed" signal.'''

            self.gui.check_errors()
