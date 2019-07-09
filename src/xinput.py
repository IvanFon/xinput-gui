from typing import Dict, List, Union
import re
import subprocess

def get_devices() -> List[Dict[str, Union[str, int]]]:
    device_id_cmd = 'xinput list --id-only'
    device_id_out = subprocess.check_output(device_id_cmd, shell=True)
    device_ids = device_id_out.decode('utf-8').splitlines()

    devices = []

    for device_id in device_ids:
        device_name_cmd = 'xinput list --name-only {}'.format(device_id)
        device_name_out = subprocess.check_output(device_name_cmd, shell=True)
        device_name = device_name_out.decode('utf-8').rstrip('\n')

        device_type_cmd ='xinput list --short {}'.format(device_id)
        device_type_out = subprocess.check_output(device_type_cmd, shell=True)
        matches = re.search(r'\[(.+)\(.+\)\]', device_type_out.decode('utf-8'))
        device_type = matches.group(1).strip()

        devices.append({
            'id': device_id,
            'name': device_name,
            'type': device_type,
            })
    
    return devices

def get_device_props(device_id: int) -> List[Dict[str, str]]:
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
            'id': matches.group(2).strip(),
            'val': matches.group(3).strip(),
            })
    
    return props

def set_device_prop(device_id: int, prop_id: int, prop_val: str):
    cmd = 'xinput set-prop {} {} {}'.format(device_id, prop_id, prop_val)
    cmd_out = subprocess.check_output(cmd, shell=True).decode('utf-8')
    
    # Print command output while there's no error handling
    print(cmd)
    print(cmd_out)

