# Fruity Menu
Build a simple UI in CircuitPython. Designed for the Adafruit RP2040 Macropad, but usable with any `displayio.Display`.

## The `Menu`
The most important class is the `Menu`. Instantiate one to get started, then use helper methods
to add options and submenus.

```py
menu = Menu(display, title='Main Menu')
menu.add_action_button('Shut down', action=myobj.dafunc)

sub_settings = Menu(display, title='Settings')
menu.add_submenu_button('Open Settings...', sub_settings)
```

