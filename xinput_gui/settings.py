# settings.py - application settings
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

'''Application settings.'''

import json

from pkg_resources import resource_filename


class Settings:
    '''Loads and stores application settings.'''

    def __init__(self):
        self.config = {}

        self.hide_prop_ids = True

        self.load_config()

    def load_config(self):
        '''Load config file.'''

        with open(resource_filename('xinput_gui', 'config.json')) as config_file:
            self.config = json.load(config_file)

        self.hide_prop_ids = self.config['hide_prop_ids']

    def save_config(self):
        '''Save config file.'''

        self.config['hide_prop_ids'] = self.hide_prop_ids

        with open(resource_filename('xinput_gui', 'config.json'),
                  'w', encoding='utf-8') as config_file:
            json.dump(self.config, config_file, indent=2)
