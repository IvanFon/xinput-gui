# __main__.py - app entry point
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

'''App entry point.'''

import pkg_resources

from .gui import Gui
from .settings import Settings


def main():
    '''Start xinput-gui.'''
    settings = Settings()

    Gui(settings)
