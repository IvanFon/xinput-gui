# prop_list.py - prop list
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

'''Device properties list.'''

from typing import TYPE_CHECKING

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename

from ..settings import Settings
from ..xinput.devices import Device, Prop
from ..xinput.xinput import Xinput
from .dialog_edit import EditDialog

if TYPE_CHECKING:
    from .win_main import MainWindow


class PropList:
    '''Device properties list.'''

    def __init__(self, main_window: 'MainWindow', settings: Settings, xinput: Xinput) -> None:
        '''Init PropList.'''

        self.main_window = main_window
        self.settings = settings
        self.xinput = xinput

        builder = self.get_builder()

        builder.connect_signals(PropList.SignalHandler(self))

        self.grid_prop_list = builder.get_object('grid_prop_list')
        self.store_props = builder.get_object('store_props')
        self.tree_props = builder.get_object('tree_props')
        self.tree_props_selection = builder.get_object(
            'tree_props_selection')
        self.tree_column_props_id = builder.get_object(
            'tree_column_props_id')
        self.cell_prop_val = builder.get_object('cell_prop_val')
        self.tool_edit_prop = builder.get_object('tool_edit_prop')
        self.tool_refresh_props = builder.get_object('tool_refresh_props')

        self.edit_dialog = EditDialog(self, xinput)

    def get_builder(self) -> Gtk.Builder:
        '''Get prop list Gtk Builder.'''

        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('xinput_gui', 'res/xinput-gui.ui'),
            ['grid_prop_list', 'store_props'])
        return builder

    def apply_settings(self) -> None:
        '''Apply current settings.'''

        # Hide prop IDs
        self.tree_column_props_id.set_visible(not self.settings.hide_prop_ids)
        # Inline prop editing
        self.cell_prop_val.set_property('editable', self.settings.inline_prop_edit)

    def show_device_props(self, device: Device) -> None:
        '''Show device properties.

        Args:
            device: Device to display props of.
        '''

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

    def refresh_props(self) -> None:
        '''Refresh properties of currently selected device.'''

        selected_device = self.main_window.device_list.get_selected_device()
        selected_device.get_props()
        self.main_window.device_list.show_device(selected_device)

    def get_selected_prop(self) -> Prop:
        '''Get the currently selected property.

        Returns:
            Selected Prop.
        '''

        model, treeiter = self.tree_props_selection.get_selected()
        return Prop(
            model[treeiter][0],
            model[treeiter][1],
            model[treeiter][2],
        )

    def set_prop(self, new_val: str) -> None:
        '''Set the value of the currently selected device property.

        Args:
            new_val: New value for the property.
        '''

        device = self.main_window.device_list.get_selected_device()
        prop = self.get_selected_prop()

        # Update prop
        device.set_prop(prop.id, new_val)

        # Update displayed value
        model, treeiter = self.tree_props_selection.get_selected()
        model[treeiter][2] = new_val

    def show_edit_dialog(self) -> None:
        '''Show the edit prop dialog.'''

        device = self.main_window.device_list.get_selected_device()
        prop = self.get_selected_prop()

        res = self.edit_dialog.show(device, prop)
        if res == Gtk.ResponseType.APPLY:
            self.refresh_props()

    class SignalHandler:
        '''Handle prop list signals.'''

        def __init__(self, gui) -> None:
            '''Init SignalHandler.'''

            self.gui = gui

        def on_tree_props_selection_changed(self, *args) -> None:
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

        def on_tool_edit_prop_clicked(self, *args) -> None:
            '''tool_edit_prop "clicked" signal.'''

            self.gui.show_edit_dialog()

        def on_tool_refresh_props_clicked(self, *args) -> None:
            '''tool_refresh_props "clicked" signal.'''

            self.gui.refresh_props()
