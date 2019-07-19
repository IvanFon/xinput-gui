# xinput.py - xinput wrapper
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

'''xinput wrapper.'''

import re
import subprocess

from .devices import Device, DeviceType


class Xinput():
    '''xinput wrapper.'''

    def __init__(self) -> None:
        '''Init Xinput.'''

        self.devices = []

        self.get_devices()

    def get_devices(self) -> None:
        '''Get xinput devices.'''

        self.devices.clear()

        device_id_cmd = 'xinput list --id-only'
        device_id_out = subprocess.check_output(device_id_cmd, shell=True)
        device_ids = device_id_out.decode('utf-8').splitlines()
        device_ids = map(lambda x: re.search(r'\D*(\d+)\D*', x).group(1), device_ids)

        for device_id in device_ids:
            device_name_cmd = 'xinput list --name-only {}'.format(device_id)
            device_name_out = subprocess.check_output(device_name_cmd, shell=True)
            device_name = device_name_out.decode('utf-8').rstrip('\n')

            device_type_cmd = 'xinput list --short {}'.format(device_id)
            device_type_out = str(subprocess.check_output(device_type_cmd, shell=True))
            if 'floating' in device_type_out:
                device_type = DeviceType.FLOATING
            elif 'pointer' in device_type_out:
                device_type = DeviceType.POINTER
            else:
                device_type = DeviceType.KEYBOARD

            device_master = 'master' in device_type_out

            self.devices.append(Device(device_id, device_name, device_type, device_master))

    def get_device_by_id(self, id_: int) -> Device:
        '''Get a device by it's ID.

        Args:
            id_: xinput device ID.
        '''

        for device in self.devices:
            if int(device.id) == id_:
                return device

        return None

    def create_master_device(self, name: str) -> None:
        '''Create a new xinput master device.

        Args:
            name: new device name.
        '''
        cmd = 'xinput create-master "{}"'.format(name)
        cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # TODO: proper error handling
        print(cmd)
        print(cmd_out)

        self.get_devices()

    def remove_master_device(self, id_: int) -> None:
        '''Remove a master xinput device.

        Args:
            id_: ID of xinput master device to remove.
        '''

        cmd = 'xinput remove-master {}'.format(id_)
        cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # TODO: proper error handling
        print(cmd)
        print(cmd_out)

        self.get_devices()
