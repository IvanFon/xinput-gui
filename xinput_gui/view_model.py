# view_model.py - app view model
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

'''App view model.'''

from typing import TYPE_CHECKING, List

from .xinput.devices import Device, Prop
from .xinput.xinput import Xinput

if TYPE_CHECKING:
    from .view_controller import ViewController


class ViewModel:
    '''App view model.'''

    def __init__(self, controller: 'ViewController') -> None:
        '''Init ViewModel.'''

        self.xinput = Xinput()

        # Currently selected device
        self.selected_device = None
        # Currently selected device property
        self.selected_prop = None
        # If currently refreshing devices
        self.refreshing = False

    def refresh_devices(self) -> List[Device]:
        '''Refresh devices.

        Returns: List of Devices.
        '''

        self.xinput.get_devices()
        return self.xinput.devices

    def set_selected_device(self, id_: int) -> None:
        '''Set selected device by ID.'''

        self.selected_device = self.xinput.get_device_by_id(id_)

    def set_selected_prop(self, id_: int, name: str, val: str) -> None:
        '''Set selected device property.

        Args:
            id_: Property ID.
            name: Property name.
            val: Property value.
        '''

        self.selected_prop = Prop(id_, name, val)

    def create_master_device(self, new_master_name: str) -> None:
        '''Create a master device.

        Args:
            new_master_name: Name of new master device.
        '''

        self.xinput.create_master_device(new_master_name)

    def remove_selected_master_device(self) -> None:
        '''Remove selected master device.'''

        self.xinput.remove_master_device(self.selected_device)

    def float_selected_device(self) -> None:
        '''Float selected device.'''

        self.selected_device.float()

    def reattach_selected_device(self, master_id: int) -> None:
        '''Reattach selected device to given master device.

        Args:
            master_id: ID of master device to reattach selected device to.
        '''

        self.selected_device.reattach(master_id)

    def set_selected_device_prop(self, new_val: str) -> None:
        '''Set selected device property.

        Args:
            new_val: New value for the property.
        '''

        self.selected_device.set_prop(self.selected_prop.id, new_val)
