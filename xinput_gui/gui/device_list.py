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

from typing import TYPE_CHECKING

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..settings import Settings
from ..xinput.devices import Device, DeviceType
from ..xinput.xinput import Xinput
from .dialog_create_master import CreateMasterDialog
from .dialog_device_info import DeviceInfoDialog
from .dialog_reattach import ReattachDialog

if TYPE_CHECKING:
    from .win_main import MainWindow


class DeviceList:
    '''Device list.'''

    def __init__(self, main_window: 'MainWindow', settings: Settings, xinput: Xinput) -> None:
        '''Init DeviceList.'''

        self.main_window = main_window
        self.settings = settings
        self.xinput = xinput
        self.refreshing = False

        builder = self.get_builder()

        builder.connect_signals(DeviceList.SignalHandler(self))

        self.grid_device_list = builder.get_object('grid_device_list')
        self.store_devices = builder.get_object('store_devices')
        self.tree_devices = builder.get_object('tree_devices')
        self.tree_devices_selection = builder.get_object(
            'tree_devices_selection')
        self.tree_column_devices_id = builder.get_object(
            'tree_column_devices_id')
        self.tool_remove_master = builder.get_object('tool_remove_master')
        self.tool_reattach_slave = builder.get_object('tool_reattach_slave')

        self.create_master_dialog = CreateMasterDialog(self, xinput)
        self.dialog_device_info = DeviceInfoDialog(self)
        self.dialog_reattach = ReattachDialog(self, xinput)

        self.refresh_devices()

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

    def get_selected_device(self) -> Device:
        '''Get the currently selected device.

        Returns:
            Currently selected Device.
        '''

        model, treeiter = self.tree_devices_selection.get_selected()

        if not treeiter:
            return None

        return self.xinput.get_device_by_id(model[treeiter][0])

    def refresh_devices(self) -> None:
        '''Refresh the device list.'''

        self.refreshing = True

        self.xinput.get_devices()

        self.store_devices.clear()
        #  self.store_props.clear()
        self.tree_devices_selection.unselect_all()
        #  self.tree_props_selection.unselect_all()
        self.tool_remove_master.set_sensitive(False)
        #  self.tool_edit_prop.set_sensitive(False)
        #  self.tool_refresh_props.set_sensitive(False)

        master_iter = None
        floating_devices = []
        for device in self.xinput.devices:
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

        self.refreshing = False

    def show_device(self, device: Device) -> None:
        '''Display properties of selected device.

        Args:
            device: Device to show.
        '''

        if device is None:
            return

        # Show props

        self.main_window.prop_list.show_device_props(device)

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

    def show_create_master_dialog(self) -> None:
        '''Show the create master device dialog.'''

        res = self.create_master_dialog.show()
        if res == Gtk.ResponseType.APPLY:
            self.refresh_devices()

    def remove_selected_master(self) -> None:
        '''Remove selected master device.'''

        device = self.get_selected_device()

        if not device.master:
            return

        self.xinput.remove_master_device(device)
        self.refresh_devices()

    def show_reattach_dialog(self) -> None:
        '''Show the reattach dialog.'''

        res = self.dialog_reattach.show(self.get_selected_device())
        if res == Gtk.ResponseType.APPLY:
            self.refresh_devices()

    def show_device_info_dialog(self) -> None:
        '''Show the device info dialog.'''

        self.dialog_device_info.show(self.get_selected_device())

    class SignalHandler:
        '''Handle device list signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_tree_devices_selection_changed(
                self,
                selection: Gtk.TreeSelection) -> None:
            '''tree_devices_selection "changed" signal.'''

            if self.gui.refreshing:
                return

            self.gui.show_device(self.gui.get_selected_device())

        def on_tool_create_master_clicked(self, *args) -> None:
            '''tool_create_master "clicked" signal.'''

            self.gui.show_create_master_dialog()

        def on_tool_remove_master_clicked(self, *args) -> None:
            '''tool_remove_master "clicked" signal.'''

            self.gui.remove_selected_master()

        def on_tool_reattach_slave_clicked(self, *args) -> None:
            '''tool_reattach_slave "clicked" signal.'''

            self.gui.show_reattach_dialog()

        def on_tool_device_info_clicked(self, *args) -> None:
            '''tool_device_info "clicked" signal.'''

            self.gui.show_device_info_dialog()

        def on_tool_refresh_devices_clicked(self, *args) -> None:
            '''tool_refresh_devices "clicked" signal.'''

            self.gui.refresh_devices()
