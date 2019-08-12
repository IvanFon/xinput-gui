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

from .gui.dialog_create_master import CreateMasterDialog
from .gui.dialog_device_info import DeviceInfoDialog
from .gui.dialog_edit import EditDialog
from .gui.dialog_reattach import ReattachDialog
from .gui.win_main import MainWindow
from .settings import Settings
from .view_model import ViewModel


class ViewController:
    '''App view controller.'''

    def __init__(self) -> None:
        '''Init ViewController.'''

        self.model = ViewModel(self)
        self.settings = Settings()
        self.main_window = MainWindow(self, self.settings)
        self.device_list = self.main_window.device_list
        self.prop_list = self.main_window.prop_list
        self.log = self.main_window.log

        self.model.xinput.set_controller(self)

        self.dialog_create_master = CreateMasterDialog(self, self.main_window)
        self.dialog_device_info = DeviceInfoDialog(self, self.main_window)
        self.dialog_edit = EditDialog(self, self.main_window)
        self.dialog_reattach = ReattachDialog(self, self.main_window)

    def start(self) -> None:
        '''Start app.'''

        self.refresh_devices()

        Gtk.main()

    def log_updated(self, log_text: str) -> None:
        '''Xinput log updated.

        Args:
            log_text: Updated log text.
        '''

        self.log.update(log_text)

    def refresh_devices(self) -> None:
        '''Refresh devices.'''

        self.model.refreshing = True

        devices = self.model.refresh_devices()
        self.device_list.refresh_devices(devices)

        self.model.refreshing = False

    def device_selected(self, id_: int) -> None:
        '''Device was selected.

        Args:
            id_: Selected device ID.
        '''

        if self.model.refreshing:
            return

        self.model.set_selected_device(id_)

        self.device_list.show_device(self.model.selected_device)
        self.prop_list.show_device_props(self.model.selected_device)

    def show_create_master_dialog(self) -> None:
        '''Show create master dialog.'''

        res = self.dialog_create_master.show()
        if res == Gtk.ResponseType.APPLY:
            self.refresh_devices()

    def create_master_device(self, new_master_name: str) -> None:
        '''Create a master device.

        Args:
            new_master_name: Name of new master device.
        '''

        self.model.create_master_device(new_master_name)

    def remove_selected_master_device(self) -> None:
        '''Remove selected master device.'''

        self.model.remove_selected_master_device()
        self.refresh_devices()

    def show_reattach_dialog(self) -> None:
        '''Show float/reattach dialog.'''

        res = self.dialog_reattach.show(self.model.selected_device,
                                        self.model.xinput.devices)
        if res == Gtk.ResponseType.APPLY:
            self.refresh_devices()

    def float_selected_device(self) -> None:
        '''Float selected device.'''

        self.model.float_selected_device()

    def reattach_selected_device(self, master_id: int) -> None:
        '''Reattach selected device to given master device.

        Args:
            master_id: ID of master device to reattach selected device to.
        '''

        self.model.reattach_selected_device(master_id)

    def show_device_info(self) -> None:
        '''Show selected device info.'''

        self.dialog_device_info.show(self.model.selected_device)

    def refresh_props(self) -> None:
        '''Refresh selected device properties.'''

        self.model.selected_device.get_props()
        self.prop_list.show_device_props(self.model.selected_device)

    def prop_selected(self, id_: int, name: str, val: str) -> None:
        '''Set selected device property.

        Args:
            id_: Property ID.
            name: Property name.
            val: Property value.
        '''

        self.model.set_selected_prop(id_, name, val)
        self.prop_list.enable_edit_tool()

    def show_edit_dialog(self) -> None:
        '''Show property edit dialog.

        Args:
            prop: Property being edited.
        '''

        res = self.dialog_edit.show(self.model.selected_device,
                                    self.model.selected_prop)
        if res == Gtk.ResponseType.APPLY:
            self.refresh_props()

    def set_prop(self, new_val: str) -> None:
        '''Set the value of the currently selected device property.

        Args:
            new_val: New value for the property.
        '''

        self.model.set_selected_device_prop(new_val)
        self.refresh_props()
