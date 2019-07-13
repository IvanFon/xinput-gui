# gui.py - graphical user interface
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

'''Graphical user interface.'''

from typing import Dict, Union

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pkg_resources import resource_filename, require

from .settings import Settings
from .xinput import get_devices, get_device_props, set_device_prop


__version__ = require('xinput_gui')[0].version


class Gui:
    def __init__(self, settings: Settings):
        self.settings = settings

        # Create interface
        builder = self.get_builder()

        builder.connect_signals(Gui.SignalHandler(self))

        # Main window widgets
        self.win_app = builder.get_object("win_app")
        self.box_main = builder.get_object("box_main")
        self.btn_edit = builder.get_object("btn_edit")
        self.store_devices = builder.get_object("store_devices")
        self.store_props = builder.get_object("store_props")
        self.tree_devices_selection = builder.get_object(
            "tree_devices_selection")
        self.tree_props_selection = builder.get_object(
            "tree_props_selection")
        self.tree_column_devices_id = builder.get_object(
            "tree_column_devices_id")
        self.tree_column_props_id = builder.get_object(
            "tree_column_props_id")

        # Edit window widgets
        self.dialog_edit = builder.get_object("dialog_edit")
        self.entry_old_val = builder.get_object("entry_old_val")
        self.entry_new_val = builder.get_object("entry_new_val")
        self.btn_edit_cancel = builder.get_object("btn_edit_cancel")
        self.btn_edit_apply = builder.get_object("btn_edit_apply")

        # Settings window widgets
        self.win_settings = builder.get_object("win_settings")
        self.btn_settings_save = builder.get_object("btn_settings_save")
        self.chk_vertical_layout = builder.get_object("chk_vertical_layout")
        self.chk_hide_device_ids = builder.get_object("chk_hide_device_ids")
        self.chk_hide_prop_ids = builder.get_object("chk_hide_prop_ids")

        self.refresh_devices()
        self.win_app.set_title("Xinput GUI {}".format(__version__))
        self.win_app.show_all()

        # About window widgets
        self.win_about = builder.get_object("win_about")
        self.win_about.set_version(__version__)

        self.apply_settings()

        Gtk.main()

    def get_builder(self):
        return Gtk.Builder().new_from_file(resource_filename('xinput_gui', 'xinput-gui.ui'))

    def refresh_devices(self):
        self.store_devices.clear()
        self.store_props.clear()
        self.tree_devices_selection.unselect_all()
        self.tree_props_selection.unselect_all()
        self.btn_edit.set_sensitive(False)

        for device in get_devices():
            self.store_devices.append([
                int(device['id']),
                device['name'],
                device['type']
            ])

    def show_device(self, device_id: int):
        self.store_props.clear()
        self.tree_props_selection.unselect_all()
        self.btn_edit.set_sensitive(False)

        for prop in get_device_props(device_id):
            self.store_props.append([
                int(prop['id']),
                prop['name'],
                prop['val']
            ])

    def get_selected_device(self) -> Dict[str, Union[str, int]]:
        model, treeiter = self.tree_devices_selection.get_selected()

        if not treeiter:
            return({
                'id': None,
                'name': None,
                'type': None,
            })

        return({
            'id': model[treeiter][0],
            'name': model[treeiter][1],
            'type': model[treeiter][2],
        })

    def get_selected_prop(self) -> Dict[str, Union[str, int]]:
        model, treeiter = self.tree_props_selection.get_selected()
        return({
            'id': model[treeiter][0],
            'name': model[treeiter][1],
            'val': model[treeiter][2],
        })

    def show_settings_window(self):
        # Get settings and update controls
        self.chk_vertical_layout.set_active(self.settings.vertical_layout)
        self.chk_hide_device_ids.set_active(self.settings.hide_device_ids)
        self.chk_hide_prop_ids.set_active(self.settings.hide_prop_ids)

        self.btn_settings_save.set_sensitive(False)
        self.win_settings.show_all()

    def apply_settings(self):
        # Vertical layout
        if self.settings.vertical_layout:
            self.box_main.set_orientation(Gtk.Orientation.VERTICAL)
            self.win_app.resize(600, 600)
        else:
            self.box_main.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.win_app.resize(800, 400)

        # Hide device IDs
        self.tree_column_devices_id.set_visible(not self.settings.hide_device_ids)
        # Hide prop IDs
        self.tree_column_props_id.set_visible(not self.settings.hide_prop_ids)

    def save_settings(self):
        # Get settings
        self.settings.vertical_layout = self.chk_vertical_layout.get_active()
        self.settings.hide_device_ids = self.chk_hide_device_ids.get_active()
        self.settings.hide_prop_ids = self.chk_hide_prop_ids.get_active()

        self.settings.save_config()

        self.apply_settings()

    class SignalHandler:
        def __init__(self, gui):
            self.gui = gui

        # Main window signals

        def on_win_app_destroy(self, *args):
            Gtk.main_quit()

        def on_menu_settings_activate(self, menu: Gtk.MenuItem):
            self.gui.show_settings_window()

        def on_menu_about_activate(self, menu: Gtk.MenuItem):
            self.gui.win_about.run()

        def on_btn_refresh_clicked(self, button: Gtk.Button):
            self.gui.refresh_devices()

        def on_device_selected(self, selection: Gtk.TreeSelection):
            selected_device = self.gui.get_selected_device()

            if selected_device['id'] == None: return

            self.gui.show_device(selected_device['id'])

        def on_prop_selected(self, selection: Gtk.TreeSelection):
            self.gui.btn_edit.set_sensitive(True)

        def on_tree_props_row_activated(self,
                                        tree: Gtk.TreeView,
                                        index: int,
                                        column: Gtk.TreeViewColumn):
            self.gui.btn_edit.clicked()

        def on_btn_edit_clicked(self, button: Gtk.Button):
            device = self.gui.get_selected_device()
            prop = self.gui.get_selected_prop()

            # Setup dialog
            self.gui.dialog_edit.get_message_area().get_children()[
                0].set_label(device['name'])
            self.gui.dialog_edit.get_message_area().get_children()[
                1].set_label(prop['name'])
            self.gui.entry_old_val.set_text(prop['val'])
            self.gui.entry_new_val.set_text(prop['val'])
            self.gui.entry_new_val.grab_focus()

            # Show dialog

            res = self.gui.dialog_edit.run()
            if res == Gtk.ResponseType.APPLY:
                new_prop_val = self.gui.entry_new_val.get_text()

                # Update prop
                set_device_prop(device['id'], prop['id'], new_prop_val)

                # Update store
                model, treeiter = self.gui.tree_props_selection.get_selected()
                model[treeiter][2] = new_prop_val

            self.gui.dialog_edit.hide()

        # Edit window signals

        def on_entry_new_val_activate(self, entry: Gtk.Entry):
            self.gui.btn_edit_apply.clicked()

        # Settings window signals

        def on_btn_settings_save_clicked(self, button: Gtk.Button):
            self.gui.save_settings()
            self.gui.win_settings.hide()

        def on_btn_settings_cancel_clicked(self, button: Gtk.Button):
            self.gui.win_settings.hide()

        def on_setting_changed(self, _):
            self.gui.btn_settings_save.set_sensitive(True)

        # About window signals

        def on_win_about_response(self, a, b):
            # TODO: close this properly
            self.gui.win_about.hide()
