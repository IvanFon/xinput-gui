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

from typing import TYPE_CHECKING
import re
import subprocess

from .devices import Device, DeviceType

if TYPE_CHECKING:
    from ..view_controller import ViewController


class Xinput():
    '''xinput wrapper.'''

    def __init__(self) -> None:
        '''Init Xinput.'''

        self.devices = []
        self.log = ''

    def set_controller(self, controller: 'ViewController') -> None:
        self.controller = controller

    def run_command(self, cmd) -> str:
        '''Run a command.

        Returns:
            Command output.
        '''

        cmd_out = subprocess.run(cmd.split(' '),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        cmd_out = cmd_out.stdout.decode('utf-8')

        # Update log
        self.log += 'COMMAND:\n'
        self.log += cmd
        self.log += '\nOUTPUT:\n'
        self.log += cmd_out
        self.log += '\n\n========== SEPARATOR ==========\n\n'

        self.controller.log_updated()

        return cmd_out

    def get_devices(self) -> None:
        '''Get xinput devices.'''

        self.devices.clear()

        device_id_cmd = 'xinput list --id-only'
        device_ids = self.run_command(device_id_cmd).splitlines()
        device_ids = map(lambda x: re.search(r'\D*(\d+)\D*', x).group(1), device_ids)

        for device_id in device_ids:
            device_name_cmd = 'xinput list --name-only {}'.format(device_id)
            device_name_out = self.run_command(device_name_cmd)
            device_name = device_name_out.rstrip('\n')

            device_type_cmd = 'xinput list --short {}'.format(device_id)
            device_type_out = self.run_command(device_type_cmd)
            if 'floating' in device_type_out:
                device_type = DeviceType.FLOATING
            elif 'pointer' in device_type_out:
                device_type = DeviceType.POINTER
            else:
                device_type = DeviceType.KEYBOARD

            device_master = 'master' in device_type_out

            self.devices.append(Device(self,
                                       device_id,
                                       device_name,
                                       device_type,
                                       device_master))

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
        self.run_command(cmd)

        self.get_devices()

    def remove_master_device(self, device: Device) -> None:
        '''Remove a master xinput device.

        Args:
            device: Master Device to remove.
        '''

        if not device.master:
            return

        cmd = 'xinput remove-master {}'.format(device.id)
        self.run_command(cmd)

        self.get_devices()
