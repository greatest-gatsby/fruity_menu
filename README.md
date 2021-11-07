# Fruity Menu
[![pipeline status](https://git.therode.net/jrode/fruity_menu/badges/main/pipeline.svg)](https://git.therode.net/jrode/fruity_menu/-/commits/main)


Build a simple UI in CircuitPython. Designed for the Adafruit RP2040 Macropad, but usable with any `displayio.Display`.

## The `Menu`
The most important class is the `Menu`. Instantiate one to get started, then use helper methods
to add options and submenus.

**Available menu options**
-  `ActionButton`: Invoke the given function with optional arguments
-  `SubmenuButton`: Open another menu as a nested submenu
-  `ValueButton`: Adjust the value of a boolean or numeric variable

```py
menu = Menu(display, title='Main Menu')
menu.add_action_button('Shut down', action=myobj.dafunc)

sub_settings = menu.create_menu('Settings')
sub_settings.add_value_button('Screen brightness', screen.brightness, update_screen_brightness)
menu.add_submenu_button('Open Settings...', sub_settings)
```

In the above example, a Menu is created and from that menu, buttons and submenus are added.
To complete the implementation of this menu, you would need to provide functions `myobj.dafunc`
and `update_screen_brightness` as well as the `screen.brightness` object used in the Value button.
These fields presumably come from the code you are using the menu for, so use as you see fit.