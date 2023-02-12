# Fruity Menu
[![pipeline status](https://git.therode.net/jrode/fruity_menu/badges/main/pipeline.svg)](https://git.therode.net/jrode/fruity_menu/-/commits/main)
[![coverage report](https://git.therode.net/jrode/fruity_menu/badges/main/coverage.svg)](https://git.therode.net/jrode/fruity_menu/-/commits/main)


Fruity Menu is a library for building simple UI menus for CircuitPython-powered devices.

### Features
-  Automatic pagination
-  Submenus w/ configurable 'Back' buttons
-  Value adjusting menus for supported types (`int`, `float`, and `bool`)
-  Buttons and menus support a number of callbacks
-  Redraw only on user input

# Usage
## The `Menu`
The most important class is the `Menu`. Instantiate one to get started, then use helper methods
to add options and submenus.

**Available menu options**
-  `ActionButton`: Invoke the given function with optional arguments
-  `SubmenuButton`: Open another menu as a nested submenu
-  `ValueButton`: Adjust the value of a boolean or numeric variable

```py
menu = Menu(display, title='Main Menu')
menu.add_action_button('Shut down', action=microcontroller.reset)

sub_settings = menu.create_menu('Settings')
sub_settings.add_value_button('Screen brightness', screen.brightness, update_screen_brightness)
menu.add_submenu_button('Open Settings...', sub_settings)
```

In the above menu, clicking 'Shut down' would invoke the CPython `reset()` function. Clicking 'Screen brightness' would open a screen for adjusting the value of `screen.brightness` and, once set, would invoke the function `update_screen_brightness` with the updated value. Note that the specified callback is responsible for "setting" the new value; the adjust menu only provides an interface for users to select a new value but does not itself update the named variable.

## Supplying inputs
Fruity Menus are navigated using `Menu.scroll(delta)` and `Menu.click()`. When scrolling, `delta` is the number of menu items to advance; a negative `delta` scrolls the other way.

Your code has to tell the top-level `Menu` when clicks and scrolls occur. Fruity Menu propagates these inputs down to whatever submenu or button may be open/selected and takes the corresponding action, including redrawing the screen. For most uses, you will want to check for your inputs every tick and invoke `Menu` functions as needed:

```py
enter_button = Button(...)
menu = Menu(...)

while True:
    if enter_button.pressed:
        menu.click()
```

A rotary encoder, such as found on the Adafruit RP2040 MacroPad, can be used for scrolling by calculating scroll delta between ticks:

```py
scroller = Encoder(...)
menu = Menu(...)

last_scroll_position = scroller.position
while True:
    if scroller.position is not last_scroll_position:
        delta = scroller.position - last_scroll_position
        last_scroll_position = scroller.position
        menu.scroll(delta)
```

Digital inputs, like buttons, can simply invoke these functions whenever pressed:

```py
up_button = Button(...)
down_button = Button(...)
enter_button = Button(...)
menu = Menu(...)

while True:
    if up_button.pressed:
        menu.scroll(1)
    
    if down_button.pressed:
        menu.scroll(-1)

    if enter_button.pressed:
        menu.click()
```