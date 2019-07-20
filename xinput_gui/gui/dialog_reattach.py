# dialog_reattach.py - reattach dialog
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

'''Reattach dialog.'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..xinput.devices import DeviceType
from ..xinput.xinput import Xinput


class ReattachDialog:
    '''Reattach dialog.'''

    def __init__(self, main_window, xinput: Xinput) -> None:
        '''Init ReattachDialog.'''

        self.main_window = main_window
        self.xinput = xinput

        builder = self.get_builder()

        self.dialog_reattach = builder.get_object('dialog_reattach')
        self.rad_float_device = builder.get_object('rad_float_device')
        self.rad_reattach_device = builder.get_object('rad_reattach_device')
        self.cmb_reattach_device = builder.get_object('cmb_reattach_device')
        self.store_reattach = builder.get_object('store_reattach')

        self.dialog_reattach.set_transient_for(main_window.win_main)

    def get_builder(self) -> Gtk.Builder:
        '''Get reattach dialog Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['dialog_reattach', 'store_reattach'])
        return builder

    def show(self, selected_device) -> None:
        '''Show the reattach dialog.

        Args:
            selected_device: device being shown.
        '''

        device = self.xinput.get_device_by_id(selected_device['id'])

        # Setup dialog

        labels = self.dialog_reattach.get_message_area().get_children()
        labels[1].set_label(selected_device['name'])
        self.rad_float_device.set_sensitive(not device.type == DeviceType.FLOATING)
        self.rad_float_device.set_active(not device.type == DeviceType.FLOATING)
        self.rad_reattach_device.set_sensitive(False)
        self.rad_reattach_device.set_active(device.type == DeviceType.FLOATING)

        self.store_reattach.clear()
        for d in self.xinput.devices:
            self.rad_reattach_device.set_sensitive(True)
            self.cmb_reattach_device.set_sensitive(True)
            self.cmb_reattach_device.set_active(0)
            if d.master:
                self.store_reattach.append([int(d.id), d.name])

        # Show dialog

        res = self.dialog_reattach.run()
        if res == Gtk.ResponseType.APPLY:
            # Float
            if self.rad_float_device.get_active():
                device.float()
            # Reattach
            else:
                master_id = self.store_reattach[self.cmb_reattach_device.get_active()][0]

                device.reattach(master_id)

            self.main_window.refresh_devices()

        self.dialog_reattach.hide()
