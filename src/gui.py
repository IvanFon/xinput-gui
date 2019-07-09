from pathlib import Path
from typing import Dict, Union
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src import xinput

class Gui:
    def __init__(self, version: str):
        # Create interface
        builder = self.get_builder()

        builder.connect_signals(Gui.SignalHandler(self))

        # Main window widgets
        self.win_app = builder.get_object("win_app")
        self.store_devices = builder.get_object("store_devices")
        self.store_props = builder.get_object("store_props")
        self.tree_devices_selection = builder.get_object("tree_devices_selection")
        self.tree_props_selection = builder.get_object("tree_props_selection")
        self.btn_edit = builder.get_object("btn_edit")
        
        self.refresh_devices()
        self.win_app.set_title('Xinput GUI {}'.format(version))
        self.win_app.show_all()

        Gtk.main()
        
    def get_builder(self):
        if Path('xinput.ui').is_file():
            return Gtk.Builder().new_from_file('xinput.ui')
        elif Path('share/xinput-gui/xinput.ui').is_file():
            return Gtk.Builder().new_from_file('share/xinput-gui/xinput.ui')
        elif Path('/usr/share/xinput-gui/xinput.ui').is_file():
            return Gtk.Builder().new_from_file('/usr/share/xinput-gui/xinput.ui')
        else:
            print('Error: xinput.ui not found')
            sys.exit()

    def refresh_devices(self):
        self.store_devices.clear()
        self.store_props.clear()
        self.tree_devices_selection.unselect_all()
        self.tree_props_selection.unselect_all()
        self.btn_edit.set_sensitive(False)

        for device in xinput.get_devices():
            self.store_devices.append([
                int(device['id']),
                device['name'],
                device['type']
                ])
    
    def show_device(self, device_id: int):
        self.store_props.clear()
        self.tree_props_selection.unselect_all()
        self.btn_edit.set_sensitive(False)
        
        for prop in xinput.get_device_props(device_id):
            self.store_props.append([
                int(prop['id']),
                prop['name'],
                prop['val']
                ])
    
    def get_selected_device(self) -> Dict[str, Union[str, int]]:
        model, treeiter = self.tree_devices_selection.get_selected()
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

    class SignalHandler:
        def __init__(self, gui):
            self.gui = gui

        def on_win_app_destroy(self, *args):
            Gtk.main_quit()

        def on_btn_close_clicked(self, button: Gtk.Button):
            Gtk.main_quit()

        def on_btn_refresh_clicked(self, button: Gtk.Button):
            self.gui.refresh_devices()

        def on_device_selected(self, selection: Gtk.TreeSelection):
            self.gui.show_device(self.gui.get_selected_device()['id'])

        def on_prop_selected(self, selection: Gtk.TreeSelection):
            self.gui.btn_edit.set_sensitive(True)

        def on_btn_edit_clicked(self, button: Gtk.Button):
            prop = self.gui.get_selected_prop()
            
            dialog = Gui.EditMessageDialog(self.gui, prop['val'])
            result = dialog.run()
            if result == Gtk.ResponseType.APPLY: # Continue
                dialog.on_btn_edit_apply_clicked()
            dialog.destroy()


    class EditMessageDialog(Gtk.MessageDialog):
        __gtype_name__ = 'EditMessageDialog'

        def __init__(self, gui, value, **kwargs):
            device_name = gui.get_selected_device()['name']
            super().__init__(modal=True, title=device_name, transient_for=gui.win_app, **kwargs)
            self.gui = gui
            self.set_resizable(True)
            prop_name = self.gui.get_selected_prop()['name']
            self.get_message_area().get_children()[0].set_label(prop_name)

            self.add_button("Cancel", Gtk.ResponseType.CANCEL)
            self.add_button("Apply", Gtk.ResponseType.APPLY)
            
            builder = self.gui.get_builder()
            grid_edit = builder.get_object("grid_edit")
            entry_old_val = builder.get_object("entry_old_val")
            self.entry_new_val = builder.get_object("entry_new_val")
            
            self.get_content_area().add(grid_edit)
            self.get_content_area().show_all()
            
            entry_old_val.set_text(value)
            self.entry_new_val.set_text(value)
            self.entry_new_val.grab_focus()

        def on_btn_edit_apply_clicked(self, *args):
            device = self.gui.get_selected_device()
            prop = self.gui.get_selected_prop()
            new_prop_val = self.entry_new_val.get_text()
            print(device)
            print(prop)

            # Update prop
            xinput.set_device_prop(device['id'], prop['id'], new_prop_val)

            # Update store
            model, treeiter = self.gui.tree_props_selection.get_selected()
            model[treeiter][2] = new_prop_val

