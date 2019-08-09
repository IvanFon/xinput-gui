# xinput-gui Usage

- [Listing devices and properties](#listing-devices-and-properties)
- [Editing properties](#editing-properties)
- [Floating and reattaching slave devices](#floating-and-reattaching-slave-devices)
- [Device info](#device-info)
- [Refreshing](#refreshing)
- [Settings](#settings)
  - [Config file](#config-file)

## Listing devices and properties

xinput-gui's interface is split into two parts: a device list, and a properties list.

When you open xinput-gui, the properties list will be blank, because no device is selected. To list the properties of a device, click on it in the device list.

The device list is displayed in a hierarchy of master and slave devices. A master device is what you see in X, such as a mouse cursor. A slave device is a physical device which controls a master device.

Every device is either a pointer or keyboard. Master devices are always pairs of a pointer and keyboard. On an average Linux system, you'll probably have one master device (one pointer and one keyboard), with all your physical devices (mice, keyboards, touchpads) attached to that master.

When you select a device in the device list, it's properties will be listed in the property list. Each property has an ID (hidden by default), a name and a value.

## Editing properties

To edit a device property, select the device and press the `Edit property` button on the device properties toolbar. A dialog will appear showing you the property's current value and allowing you to enter a new one.

If inline property editing is enabled in the settings, double-click on the property value and you can change it's value directly in the property list. Press enter to apply the change.

## Creating and removing master devices

To create a master device, click on the `Add master device` button on the device list toolbar. A dialog  will appear asking you for a name for the new master device. Once you type in a valid name, press enter/create to create the master device. You will see the new pointer and keyboard in the device list.

To remove a master device, select it in the device list. The `Remove master device` button on the device list toolbar will become active. Click on it and the selected master device will be removed.

## Floating and reattaching slave devices

Slave devices can be floating, which means not attached to any master device, or they can be reattached to a different master device.

To float or reattach a slave device, select it in the device list. The `Reattach slave device` button on the device list toolbar will be come active. Click on it, and a dialog will appear, allowing you to choose whether you want to float the device, or reattach it to a different master. When reattaching a device, you can select the master device you wish to reattach it to from the dropdown.

Floating slave devices will be displayed at the top level of the device list with type `floating`.

## Device info

To get more info about a selected device, click on the `Show device info` button on the device list toolbar. A dialog will appear containing the output of `xinput list [device]`. This contains the device's InputClasses.

## Refreshing

If the list of devices or properties has been changed while xinput-gui is running, you can use the `Refresh devices` and `Refresh properties` buttons on the device and property list toolbars to refresh their info.

The `Refresh properties` button will only become active when a device is selected.

## Settings

You can change xinput-gui's settings by clicking on `Edit -> Settings` on the menubar. The following settings are available:

- Vertical layout
  - Default value: false
  - When enabled, the window will be taller rather than wider, and the properties list will be below the device list, as opposed to beside it. This is useful for vertical monitor or split screen setups, as the vertical layout will allow more room for device and property names.
- Edit property values inline
  - Default value: true
  - When enabled, property values can be quickly edited by double-clicking on their value in the property list, without having to open the edit dialog.
- Hide device IDs
  - Default value: true
  - When enabled, device IDs will be hidden in the device list.
- Hide property IDs
  - Default value: true
  - When enabled, property IDs will be hidden in the property list.

Click `Save` to save and apply your changes, or `Cancel` to discard them.

### Config file

xinput-gui will save your settings to `$HOME/.xinput-gui.json`. To reset your settings, delete that file, and next time you launch xinput-gui, it will load the default settings and recreate the file.
