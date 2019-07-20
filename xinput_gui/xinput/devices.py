# devices.py - xinput device classes
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

'''xinput device classes.'''

from enum import Enum
import re
import subprocess


class DeviceType(Enum):
    '''Device types.'''

    FLOATING = 'floating'
    POINTER = 'pointer'
    KEYBOARD = 'keyboard'


class Prop:
    '''An xinput device property.'''

    def __init__(self, id_: int, name: str, val: str) -> None:
        '''Init Prop.

        Args:
            id_: property ID.
            name: property name.
            val: property value.
        '''

        self.id = id_
        self.name = name
        self.val = val


class Device:
    '''An xinput device.'''

    def __init__(self,
                 id_: int,
                 name: str,
                 type_: DeviceType,
                 master: bool) -> None:
        '''Init Device.

        Args:
            id_: xinput device ID.
            name: xinput device name.
            type_: xinput device type.
            master: if device is master.
        '''

        self.id = id_
        self.name = name
        self.type = type_
        self.master = master

        self.props = []

        self.get_props()

    def get_props(self) -> None:
        '''Get device properties.'''

        self.props.clear()

        props_cmd = 'xinput list-props {}'.format(self.id)
        props_out = subprocess.check_output(props_cmd, shell=True).decode('utf-8')
        props_out = props_out.splitlines()
        props_out.pop(0)
        props_out = list(map(lambda x: x.replace('\t', ''), props_out))

        for prop in props_out:
            matches = re.search(r'^(.+) \((\d+)\):(.+)$', prop)
            self.props.append(Prop(
                matches.group(2).strip(),
                matches.group(1).strip(),
                matches.group(3).strip(),
            ))

    def set_prop(self, prop_id: int, prop_val: str) -> None:
        '''Set a device property.

        Args:
            prop_id: ID of property to change.
            prop_val: new property value.
        '''

        cmd = 'xinput set-prop {} {} {}'.format(self.id, prop_id, prop_val)
        cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # TODO: error handling
        print(cmd)
        print(cmd_out)

    def float(self) -> None:
        '''Float slave device.'''

        if self.master:
            return

        cmd = 'xinput float {}'.format(self.id)
        cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # TODO: proper error handling
        print(cmd)
        print(cmd_out)

    def reattach(self, master_id: int) -> None:
        '''Reattach device to master.

        Args:
            master_id: ID of xinput master device to reattach slave device to.
        '''

        if self.master:
            return

        cmd = 'xinput reattach {} {}'.format(self.id, master_id)
        cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # TODO: proper error handling
        print(cmd)
        print(cmd_out)

    def get_info(self) -> str:
        '''Get device info.

        Returns:
            Device info.
        '''

        cmd = 'xinput list {}'.format(self.id)
        cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')

        return cmd_out
