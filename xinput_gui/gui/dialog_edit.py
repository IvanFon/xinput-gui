# dialog_edit.py - edit dialog
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

'''Edit dialog.'''

from typing import Dict, Union

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename


class EditDialog:
    '''Edit dialog.'''

    def __init__(self, main_window) -> None:
        '''Init EditDialog.'''

        self.main_window = main_window

        builder = self.get_builder()

        builder.connect_signals(EditDialog.SignalHandler(self))

        self.dialog_edit = builder.get_object('dialog_edit')
        self.entry_old_val = builder.get_object('entry_old_val')
        self.entry_new_val = builder.get_object('entry_new_val')
        self.btn_edit_cancel = builder.get_object('btn_edit_cancel')
        self.btn_edit_apply = builder.get_object('btn_edit_apply')

        self.dialog_edit.set_transient_for(main_window.win_main)

    def get_builder(self) -> Gtk.Builder:
        '''Get edit dialog Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['dialog_edit'])
        return builder

    def show(self,
             device: Dict[str, Union[str, int]],
             prop: Dict[str, Union[str, int]]) -> None:
        '''Show the edit dialog.

        Args:
            device: Device being edited.
            prop: Device property being edited.
        '''

        # Setup dialog

        labels = self.dialog_edit.get_message_area().get_children()
        labels[0].set_label(device['name'])
        labels[1].set_label(prop['name'])
        self.entry_old_val.set_text(prop['val'])
        self.entry_new_val.set_text(prop['val'])
        self.entry_new_val.grab_focus()

        # Show dialog

        res = self.dialog_edit.run()
        if res == Gtk.ResponseType.APPLY:
            new_prop_val = self.entry_new_val.get_text()

            self.main_window.set_prop(new_prop_val)

        self.dialog_edit.hide()

    class SignalHandler:
        '''Handle edit dialog signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_entry_new_val_activate(self, *args) -> None:
            '''entry_new_val "activate" signal.'''

            self.gui.btn_edit_apply.clicked()
