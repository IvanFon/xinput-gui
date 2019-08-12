# device_list.py - device list
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

'''Device list.'''

from typing import TYPE_CHECKING, List

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..settings import Settings
from ..xinput.devices import Device, DeviceType

if TYPE_CHECKING:
    from ..view_controller import ViewController
    from .win_main import MainWindow


class DeviceList:
    '''Device list.'''

    def __init__(self, controller: 'ViewController', main_window: 'MainWindow', settings: Settings) -> None:
        '''Init DeviceList.'''

        self.controller = controller
        self.main_window = main_window
        self.settings = settings
        self.refreshing = False

        builder = self.get_builder()

        builder.connect_signals(DeviceList.SignalHandler(controller))

        self.grid_device_list = builder.get_object('grid_device_list')
        self.store_devices = builder.get_object('store_devices')
        self.tree_devices = builder.get_object('tree_devices')
        self.tree_devices_selection = builder.get_object(
            'tree_devices_selection')
        self.tree_column_devices_id = builder.get_object(
            'tree_column_devices_id')
        self.tool_remove_master = builder.get_object('tool_remove_master')
        self.tool_reattach_slave = builder.get_object('tool_reattach_slave')

    def get_builder(self) -> Gtk.Builder:
        '''Get device list Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['grid_device_list', 'store_devices'])
        return builder

    def apply_settings(self) -> None:
        '''Apply current settings.'''

        # Hide device IDs
        self.tree_column_devices_id.set_visible(not self.settings.hide_device_ids)

    def refresh_devices(self, devices: List[Device]) -> None:
        '''Refresh the device list.

        Args:
            devices: List of Devices.
        '''

        self.store_devices.clear()
        self.tree_devices_selection.unselect_all()
        self.tool_remove_master.set_sensitive(False)

        master_iter = None
        floating_devices = []
        for device in devices:
            device_row = [
                int(device.id),
                device.name,
                device.type.value,
            ]

            if device.type == DeviceType.FLOATING:
                floating_devices.append(device_row)
                continue

            cur_iter = self.store_devices.append(master_iter, device_row)

            if device.master:
                self.store_devices.remove(cur_iter)
                master_iter = self.store_devices.append(None, device_row)

        for device in floating_devices:
            self.store_devices.append(None, device)

        self.tree_devices.expand_all()

    def show_device(self, device: Device) -> None:
        '''Display properties of selected device.

        Args:
            device: Device to show.
        '''

        if device is None:
            return

        # Check if device is master
        if device.master:
            self.tool_remove_master.set_sensitive(True)
            self.tool_reattach_slave.set_sensitive(False)
        else:
            self.tool_remove_master.set_sensitive(False)
            self.tool_reattach_slave.set_sensitive(True)

        # Check if device is floating
        if device.type == DeviceType.FLOATING:
            self.tool_reattach_slave.set_icon_name('gtk-connect')
        else:
            self.tool_reattach_slave.set_icon_name('gtk-disconnect')

    class SignalHandler:
        '''Handle device list signals.'''

        def __init__(self, controller: 'ViewController') -> None:
            '''Init SignalHandler.'''

            self.controller = controller

        def on_tree_devices_selection_changed(
                self,
                selection: Gtk.TreeSelection) -> None:
            '''tree_devices_selection "changed" signal.'''

            model, treeiter = selection.get_selected()

            if not treeiter:
                return

            self.controller.device_selected(model[treeiter][0])

        def on_tool_create_master_clicked(self, *args) -> None:
            '''tool_create_master "clicked" signal.'''

            self.controller.show_create_master_dialog()

        def on_tool_remove_master_clicked(self, *args) -> None:
            '''tool_remove_master "clicked" signal.'''

            self.controller.remove_selected_master_device()

        def on_tool_reattach_slave_clicked(self, *args) -> None:
            '''tool_reattach_slave "clicked" signal.'''

            self.controller.show_reattach_dialog()

        def on_tool_device_info_clicked(self, *args) -> None:
            '''tool_device_info "clicked" signal.'''

            self.controller.show_device_info()

        def on_tool_refresh_devices_clicked(self, *args) -> None:
            '''tool_refresh_devices "clicked" signal.'''

            self.controller.refresh_devices()
