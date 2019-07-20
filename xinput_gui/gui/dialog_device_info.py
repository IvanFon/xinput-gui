# dialog_device_info.py - device info dialog
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

'''Device info dialog.'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..xinput.devices import Device


class DeviceInfoDialog:
    '''Device info dialog.'''

    def __init__(self, main_window) -> None:
        '''Init DeviceInfoDialog.'''

        self.main_window = main_window

        builder = self.get_builder()

        self.dialog_device_info = builder.get_object('dialog_device_info')
        self.buffer_device_info = builder.get_object('buffer_device_info')

        self.dialog_device_info.set_transient_for(main_window.win_main)

    def get_builder(self) -> Gtk.Builder:
        '''Get device info dialog Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['dialog_device_info', 'buffer_device_info'])
        return builder

    def show(self, device: Device) -> None:
        '''Show the device info dialog.

        Args:
            device: Device whose info is being shown.
        '''

        # Setup dialog

        labels = self.dialog_device_info.get_message_area().get_children()
        labels[1].set_label(device.name)
        self.buffer_device_info.set_text(device.get_info())

        # Show dialog

        res = self.dialog_device_info.run()
        self.dialog_device_info.hide()
