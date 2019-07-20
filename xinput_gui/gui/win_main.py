# win_main.py - main app window
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

'''Main app window.'''

from typing import Dict, Union

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import require, resource_filename

from ..settings import Settings
from ..xinput.devices import DeviceType
from ..xinput.xinput import Xinput
from .dialog_about import AboutDialog
from .dialog_create_master import CreateMasterDialog
from .dialog_device_info import DeviceInfoDialog
from .dialog_edit import EditDialog
from .dialog_reattach import ReattachDialog
from .win_settings import SettingsWindow


__version__ = require('xinput_gui')[0].version


class MainWindow:
    '''Main app window.'''

    def __init__(self, settings: Settings, xinput: Xinput) -> None:
        '''Init MainWindow.'''

        self.settings = settings
        self.xinput = xinput
        self.refreshing = False

        builder = self.get_builder()

        builder.connect_signals(MainWindow.SignalHandler(self))

        self.win_main = builder.get_object('win_main')
        self.win_main = builder.get_object('win_main')
        self.box_main = builder.get_object('box_main')
        self.store_devices = builder.get_object('store_devices')
        self.store_props = builder.get_object('store_props')
        self.tree_devices = builder.get_object('tree_devices')
        self.tree_devices_selection = builder.get_object(
            'tree_devices_selection')
        self.tree_props = builder.get_object('tree_props')
        self.tree_props_selection = builder.get_object(
            'tree_props_selection')
        self.tree_column_devices_id = builder.get_object(
            'tree_column_devices_id')
        self.tree_column_props_id = builder.get_object(
            'tree_column_props_id')
        self.cell_prop_val = builder.get_object('cell_prop_val')
        self.tool_remove_master = builder.get_object('tool_remove_master')
        self.tool_reattach_slave = builder.get_object('tool_reattach_slave')
        self.tool_edit_prop = builder.get_object('tool_edit_prop')
        self.tool_refresh_props = builder.get_object('tool_refresh_props')

        self.apply_settings()

        self.refresh_devices()
        self.win_main.set_title('Xinput GUI {}'.format(__version__))
        self.win_main.show_all()

        self.about_dialog = AboutDialog(self)
        self.create_master_dialog = CreateMasterDialog(self, xinput)
        self.dialog_device_info = DeviceInfoDialog(self)
        self.dialog_reattach = ReattachDialog(self, xinput)
        self.edit_dialog = EditDialog(self)
        self.settings_window = SettingsWindow(self, settings)

        Gtk.main()

    def get_builder(self) -> Gtk.Builder:
        '''Get main window Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['win_main', 'store_devices', 'store_props'])
        return builder

    def refresh_devices(self) -> None:
        '''Refresh the device list.'''

        self.refreshing = True

        self.xinput.get_devices()

        self.store_devices.clear()
        self.store_props.clear()
        self.tree_devices_selection.unselect_all()
        self.tree_props_selection.unselect_all()
        self.tool_remove_master.set_sensitive(False)
        self.tool_edit_prop.set_sensitive(False)
        self.tool_refresh_props.set_sensitive(False)

        master_iter = None
        floating_devices = []
        for device in self.xinput.devices:
            device_row = [
                int(device.id),
                device.name,
                device.type.value,
            ]

            if device.type == DeviceType.FLOATING:
                floating_devices.append(device_row)
                continue

            cur_iter = self.store_devices.append(master_iter, device_row)

            if device.master:
                self.store_devices.remove(cur_iter)
                master_iter = self.store_devices.append(None, device_row)

        for device in floating_devices:
            self.store_devices.append(None, device)

        self.tree_devices.expand_all()

        self.refreshing = False

    def refresh_props(self) -> None:
        '''Refresh properties of currently selected device.'''

        self.xinput.get_device_by_id(self.get_selected_device()['id']).get_props()
        self.show_device(self.tree_devices_selection)
        self.tree_props.scroll_to_point(0, 0)

    def show_device(self, selection: Gtk.TreeSelection) -> None:
        '''Display properties of selected device.

        Args:
            selection: The TreeSelection for the selected device.
        '''

        model, treeiter = selection.get_selected()
        device_id = model[treeiter][0]

        if device_id is None:
            return

        device = self.xinput.get_device_by_id(device_id)

        # Show props

        self.store_props.clear()
        self.tree_props_selection.unselect_all()
        self.tool_edit_prop.set_sensitive(False)
        self.tool_refresh_props.set_sensitive(True)

        for prop in device.props:
            self.store_props.append(None, [
                int(prop.id),
                prop.name,
                prop.val,
            ])

        self.tree_props.scroll_to_point(0, 0)

        # Check if device is master
        if device.master:
            self.tool_remove_master.set_sensitive(True)
            self.tool_reattach_slave.set_sensitive(False)
        else:
            self.tool_remove_master.set_sensitive(False)
            self.tool_reattach_slave.set_sensitive(True)

        # Check if device is floating
        if device.type == DeviceType.FLOATING:
            self.tool_reattach_slave.set_icon_name('gtk-connect')
        else:
            self.tool_reattach_slave.set_icon_name('gtk-disconnect')

    def get_selected_device(self) -> Dict[str, Union[str, int]]:
        '''Get the currently selected device.

        Returns:
            A Dict containing:
                - id: device ID, int
                - name: device name, str
                - type: device type, str
                - master: if device is master, bool

            If no device is selected, all dict values will be None.
        '''

        model, treeiter = self.tree_devices_selection.get_selected()

        if not treeiter:
            return({
                'id': None,
                'name': None,
                'type': None,
                'master': None,
            })

        return({
            'id': model[treeiter][0],
            'name': model[treeiter][1],
            'type': model[treeiter][2],
            'master': self.store_devices.iter_depth(treeiter) == 0,
        })

    def get_selected_prop(self) -> Dict[str, Union[str, int]]:
        '''Get the currently selected property.

        Returns:
            A dict containing:
                - id: property ID, int
                - name: property name, str
                - val: property value, str
        '''

        model, treeiter = self.tree_props_selection.get_selected()
        return({
            'id': model[treeiter][0],
            'name': model[treeiter][1],
            'val': model[treeiter][2],
        }, model, treeiter)

    def set_prop(self, new_val: str) -> None:
        '''Set the value of the currently selected device property.

        Args:
            new_val: New value for the property.
        '''

        device = self.get_selected_device()
        prop, model, treeiter = self.get_selected_prop()

        # Update prop
        self.xinput.get_device_by_id(device['id']).set_prop(prop['id'], new_val)

        # Update store
        model[treeiter][2] = new_val

    def remove_selected_master(self) -> None:
        '''Remove selected master device.'''

        device = self.get_selected_device()

        if not device['master']:
            return

        self.xinput.remove_master_device(device['id'])

        self.refresh_devices()

    def apply_settings(self) -> None:
        '''Apply current settings.'''

        # Vertical layout
        if self.settings.vertical_layout:
            self.box_main.set_orientation(Gtk.Orientation.VERTICAL)
            self.win_main.resize(600, 600)
        else:
            self.box_main.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.win_main.resize(800, 400)

        # Inline prop editing
        self.cell_prop_val.set_property('editable', self.settings.inline_prop_edit)

        # Hide device IDs
        self.tree_column_devices_id.set_visible(not self.settings.hide_device_ids)
        # Hide prop IDs
        self.tree_column_props_id.set_visible(not self.settings.hide_prop_ids)

    def show_device_info_dialog(self) -> None:
        '''Shows the device info dialog.'''

        device = self.xinput.get_device_by_id(self.get_selected_device()['id'])
        self.dialog_device_info.show(device)

    def show_edit_dialog(self) -> None:
        '''Shows the edit dialog.'''

        device = self.get_selected_device()
        prop, _, _ = self.get_selected_prop()

        self.edit_dialog.show(device, prop)

    def show_settings_window(self) -> None:
        '''Shows the settings window.'''

        self.settings_window.show()

    def show_about_dialog(self) -> None:
        '''Shows the about dialog.'''

        self.about_dialog.show()

    def show_create_master_dialog(self) -> None:
        '''Shows the create master dialog.'''

        self.create_master_dialog.show()

    def show_reattach_dialog(self) -> None:
        '''Show the reattach dialog.'''

        self.dialog_reattach.show(self.get_selected_device())

    class SignalHandler:
        '''Handle main window signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_win_main_destroy(self, *args) -> None:
            '''win_main "destroy" signal.'''

            Gtk.main_quit()

        def on_menu_settings_activate(self, *args) -> None:
            '''menu_settings "activate" signal.'''

            self.gui.show_settings_window()

        def on_menu_about_activate(self, *args) -> None:
            '''menu_about "activate" signal.'''

            self.gui.show_about_dialog()

        def on_device_selected(self, selection: Gtk.TreeSelection) -> None:
            '''tree_devices_selection "changed" signal.'''

            if self.gui.refreshing:
                return

            self.gui.show_device(selection)

        def on_prop_selected(self, *args) -> None:
            '''tree_props_selection "changed" signal.'''

            self.gui.tool_edit_prop.set_sensitive(True)

        def on_tree_props_row_activated(self, *args) -> None:
            '''tree_props "row-activated" signal.'''

            self.gui.show_edit_dialog()

        def on_cell_prop_val_edited(self,
                                    renderer: Gtk.CellRendererText,
                                    path: str,
                                    new_text) -> None:
            '''cell_prop_val "edited" signal.'''

            self.gui.set_prop(new_text)

        def on_tool_create_master_clicked(self, *args) -> None:
            '''tool_create_master "clicked" signal.'''

            self.gui.show_create_master_dialog()

        def on_tool_remove_master_clicked(self, *args) -> None:
            '''tool_remove_master "clicked" signal.'''

            self.gui.remove_selected_master()

        def on_tool_reattach_slave_clicked(self, *args) -> None:
            '''tool_reattach_slave "clicked" signal.'''

            self.gui.show_reattach_dialog()

        def on_tool_refresh_devices_clicked(self, *args) -> None:
            '''tool_refresh_devices "clicked" signal.'''

            self.gui.refresh_devices()

        def on_tool_device_info_clicked(self, *args) -> None:
            '''tool_device_info "clicked" signal.'''

            self.gui.show_device_info_dialog()

        def on_tool_edit_prop_clicked(self, *args) -> None:
            '''tool_edit_prop "clicked" signal.'''

            self.gui.show_edit_dialog()

        def on_tool_refresh_props_clicked(self, *args) -> None:
            '''tool_refresh_props "clicked" signal.'''

            self.gui.refresh_props()
