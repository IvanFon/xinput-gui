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
from ..xinput.devices import Device

if TYPE_CHECKING:
    from ..view_controller import ViewController
    from .win_main import MainWindow


class PropList:
    '''Device properties list.'''

    def __init__(self, controller: 'ViewController', main_window: 'MainWindow', settings: Settings) -> None:
        '''Init PropList.'''

        self.controller = controller
        self.main_window = main_window
        self.settings = settings

        builder = self.get_builder()

        builder.connect_signals(PropList.SignalHandler(controller))

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

    def enable_edit_tool(self) -> None:
        '''Enable edit prop tool.'''

        self.tool_edit_prop.set_sensitive(True)

    class SignalHandler:
        '''Handle prop list signals.'''

        def __init__(self, controller) -> None:
            '''Init SignalHandler.'''

            self.controller = controller

        def on_tree_props_selection_changed(
                self,
                selection: Gtk.TreeSelection) -> None:
            '''tree_props_selection "changed" signal.'''

            model, treeiter = selection.get_selected()

            if not treeiter:
                return

            self.controller.prop_selected(
                model[treeiter][0],
                model[treeiter][1],
                model[treeiter][2],
            )

        def on_tree_props_row_activated(self, *args) -> None:
            '''tree_props "row-activated" signal.'''

            self.controller.show_edit_dialog()

        def on_cell_prop_val_edited(self,
                                    renderer: Gtk.CellRendererText,
                                    path: str,
                                    new_text) -> None:
            '''cell_prop_val "edited" signal.'''

            self.controller.set_prop(new_text)

        def on_tool_edit_prop_clicked(self, *args) -> None:
            '''tool_edit_prop "clicked" signal.'''

            self.controller.show_edit_dialog()

        def on_tool_refresh_props_clicked(self, *args) -> None:
            '''tool_refresh_props "clicked" signal.'''

            self.controller.refresh_props()
