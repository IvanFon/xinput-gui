# win_settings.py - settings window
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

'''Settings window.'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..settings import Settings


class SettingsWindow:
    '''Settings window.'''

    def __init__(self, main_window, settings: Settings) -> None:
        '''Init SettingsWindow.'''

        self.main_window = main_window
        self.settings = settings

        builder = self.get_builder()

        builder.connect_signals(SettingsWindow.SignalHandler(self))

        self.win_settings = builder.get_object('win_settings')
        self.btn_settings_save = builder.get_object('btn_settings_save')
        self.chk_vertical_layout = builder.get_object('chk_vertical_layout')
        self.chk_inline_prop_edit = builder.get_object('chk_inline_prop_edit')
        self.chk_hide_device_ids = builder.get_object('chk_hide_device_ids')
        self.chk_hide_prop_ids = builder.get_object('chk_hide_prop_ids')

        self.win_settings.set_transient_for(main_window.win_main)

    def get_builder(self) -> Gtk.Builder:
        '''Get settings window Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['win_settings'])
        return builder

    def show(self) -> None:
        '''Show the settings window.'''

        # Get settings and update controls
        self.chk_vertical_layout.set_active(self.settings.vertical_layout)
        self.chk_inline_prop_edit.set_active(self.settings.inline_prop_edit)
        self.chk_hide_device_ids.set_active(self.settings.hide_device_ids)
        self.chk_hide_prop_ids.set_active(self.settings.hide_prop_ids)

        self.btn_settings_save.set_sensitive(False)
        self.win_settings.show_all()

    def hide(self) -> None:
        '''Hide the settings window.'''

        self.win_settings.hide()

    def save_settings(self) -> None:
        '''Save settings.'''

        # Get settings
        self.settings.vertical_layout = self.chk_vertical_layout.get_active()
        self.settings.inline_prop_edit = self.chk_inline_prop_edit.get_active()
        self.settings.hide_device_ids = self.chk_hide_device_ids.get_active()
        self.settings.hide_prop_ids = self.chk_hide_prop_ids.get_active()

        # Save
        self.settings.save_config()

        # Apply
        self.main_window.apply_settings()

    class SignalHandler:
        '''Handle settings window signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_btn_settings_save_clicked(self, *args) -> None:
            '''btn_settings_save "clicked" signal.'''

            self.gui.save_settings()
            self.gui.hide()

        def on_btn_settings_cancel_clicked(self, *args) -> None:
            '''btn_edit_cancel "clicked" signal.'''

            self.gui.hide()

        def on_setting_changed(self, *args):
            '''Fired when any setting widget has been changed.'''

            self.gui.btn_settings_save.set_sensitive(True)
