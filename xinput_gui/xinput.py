# xinput.py - wrapper around xinput
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

'''Wrapper around xinput.'''

from typing import Dict, List, Union
import re
import subprocess


def get_devices() -> List[Dict[str, Union[str, int]]]:
    '''Gets a list of xinput devices.

    Returns:
        A list containing one dict entry per device. Each device has:
            - 'id': device ID, int
            - 'name': device name, str
            - 'type': device type, str
    '''

    device_id_cmd = 'xinput list --id-only'
    device_id_out = subprocess.check_output(device_id_cmd, shell=True)
    device_ids = device_id_out.decode('utf-8').splitlines()

    devices = []

    for device_id in device_ids:
        device_name_cmd = 'xinput list --name-only {}'.format(device_id)
        device_name_out = subprocess.check_output(device_name_cmd, shell=True)
        device_name = device_name_out.decode('utf-8').rstrip('\n')

        device_type_cmd = 'xinput list --short {}'.format(device_id)
        device_type_out = subprocess.check_output(device_type_cmd, shell=True)
        matches = re.search(r'\[(.+)\(.+\)\]', device_type_out.decode('utf-8'))
        device_type = matches.group(1).strip()

        devices.append({
            'id': device_id,
            'name': device_name,
            'type': device_type,
        })

    return devices


def get_device_props(device_id: int) -> List[Dict[str, Union[str, int]]]:
    '''Gets a list of properties for a given xinput device.

    Args:
        device_id: The xinput device ID.

    Returns:
        A list containing one dict entry per device property. Each property has:
            - name: property name, str
            - id: property id, int
            - val: property value, str
    '''

    props_cmd = 'xinput list-props {}'.format(device_id)
    props_out = subprocess.check_output(props_cmd, shell=True).decode('utf-8')
    props_out = props_out.splitlines()
    props_out.pop(0)
    props_out = list(map(lambda x: x.replace('\t', ''), props_out))

    props = []
    for prop in props_out:
        matches = re.search(r'^(.+) \((\d+)\):(.+)$', prop)
        props.append({
            'name': matches.group(1).strip(),
            'id': int(matches.group(2).strip()),
            'val': matches.group(3).strip(),
        })

    return props


def set_device_prop(device_id: int, prop_id: int, prop_val: str):
    '''Sets an xinput device property.

    Args:
        device_id: An xinput device ID.
        prop_id: ID of a property belonging to that device.
        prop_val: The new value for the property.
    '''

    cmd = 'xinput set-prop {} {} {}'.format(device_id, prop_id, prop_val)
    cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')

    # TODO: proper error handling
    print(cmd)
    print(cmd_out)
