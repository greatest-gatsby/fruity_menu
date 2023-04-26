# Fruity Menu
[![pipeline status](https://git.therode.net/jrode/fruity_menu/badges/main/pipeline.svg)](https://git.therode.net/jrode/fruity_menu/-/commits/main)
[![coverage report](https://git.therode.net/jrode/fruity_menu/badges/main/coverage.svg)](https://git.therode.net/jrode/fruity_menu/-/commits/main)


Fruity Menu is a library for building simple UI menus for CircuitPython-powered devices.

![Menu example](/examples/adafruit-macropad/macropad-set.png "Macropad menu")\
*Above:* Menus contain scrollable items, nestable submenus, and user-adjustable variables.

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

menu.show_menu()
```

In the above menu, clicking 'Shut down' would invoke the CPython `reset()` function. Clicking 'Screen brightness' would open a screen for adjusting the value of `screen.brightness` and, once set, would invoke the function `update_screen_brightness` with the updated value. Note that the specified callback is responsible for "setting" the new value; the adjust menu only provides an interface for users to select a new value but does not itself update the named variable. Finally, the call to `show_menu()` tells the Fruity Menu to render itself to the screen.

**Using a dict to create a menu**
You can also use a `dict` to create a menu. This can be give more readable code. The same menu as above could be created as:

```py
menu_items = {
    'Shut down': microcontroller.reset,
    'Settings': {
        'Screen brightness': Value(screen.brightness, update_screen_brightness)
    }
}
menu = Menu(display, title='Main Menu')
build_menu(menu, menu_items)

menu.show_menu()
```
Note using `Value` to provide the other arguments that would be used in `add_value_button`


## Supplying inputs
Fruity Menus are navigated using `Menu.scroll(delta)` and `Menu.click()`. When scrolling, `delta` is the number of menu items to advance; a negative `delta` scrolls the other way.

Your code has to tell the **top-level** `Menu` when clicks and scrolls occur. Fruity Menu propagates these inputs down to whatever submenu or button may be open/selected and takes the corresponding action, including redrawing the screen. For most uses, you will want to check for your inputs every tick and invoke `Menu` functions as needed:

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

## When to render
For the most part, Fruity Menu handles calls to render to the screen. For example, `click()` and `scroll(delta)` both ensure that the screen is rendered after navigating. You only need to invoke `show_menu()` when the screen wasn't already showing Fruity Menu and you want to begin showing it. This means you can use the whole screen for your application and then only open the menu when the user provides the necessary input, like clicking a button.

To best manage other applications using the same display, add an `ActionButton` to the top-level menu. For the callback, specify a function that will render your application to the screen. You will also need to track which application is "open" and route your inputs to the appropriate app.

For example, consider an application named `WeatherMonitor` that has:
- A function called `enter()` which is used to control which category of weather data it shows to the screen
- A function called `display()` which renders the selected data to the screen

```py
enter_btn: Button(...)
monitor: WeatherMonitor = WeatherMonitor()
menu: Menu = Menu(...)
menu.add_action_button('Close', monitor.display)

monitor.display()

is_in_menu: bool = False

while True:
    if enter_btn.pressed:
        if is_in_menu:
            menu.clicked()
        else:
            monitor.enter()
```

If the user clicks the `enter_btn` then the menu will be clicked if it is open; otherwise the `WeatherMonitor` will be clicked. Your application will need some mechanism of communicating its intent to open the menu by invoking `menu.show_menu()`. For example, you could add a dedicated `Button` whose only action is to toggle whether the menu is open:

```py
menu_btn: Button = Button(...)
monitor: WeatherMonitor()
menu: Menu = Menu(...)

is_in_menu: bool = False

while True:
    if menu_btn.pressed:
        is_in_menu = not is_in_menu
        if is_in_menu:
            menu.show_menu()
        else:
            monitor.display()
```

Here, the `WeatherMonitor` will "own" the screen until the menu is told to "take over".

## User-adjustable variables
Fruity Menu provides `ValueButton`s which allow users to adjust the values of variables. By adding a `ValueButton` to a menu, Fruity Menu will construct a graphical menu for adjusting the value. Users can `scroll(delta)` up and down to adjust the value, and `click()` to "set" it.

Importantly, these menus do not update the variables directly; instead, you must specify a callback when adding the button. This callback is invoked when the value is set; whatever function you set in the callback must update whatever variable you have set.

For example, consider you have a class called `Television`, an instance of that class called `tv`, and you want to add a volume adjustment button to your menu called `menu`:

```py
def set_volume(new_volume):
    tv.volume = new_volume

tv.volume = 0.0
menu.add_value_button('Volume', tv.volume, set_volume)
```

The function `set_volume(new_volume)` is supplied as a callback to `add_value_button(...)`. Once the user clicks the button and selects a new value, Fruity Menu will invoke the given function and provide the new value as its only argument. The callback is responsible for acting on the changed value.

### Supported types
-  Numbers (`int`, `float`)
-  Boolean

Numeric types can be defined with upper- and lower-bounds for acceptable values, as well as scrolling factors to control how much a single `scroll()` changes the value.

```py
menu.add_value_button('Brightness', display.brightness, update_display_brightness, scroll_factor=0.1, min_val=0.0, max_val=1.0)
```

If additional options are supplied but are not relevant (like providing `scroll_factor` for a boolean variable), then they are simply ignored. If a user attempts to `scroll(delta)` outside of the specified bounds, then the menu will limit the value to that bounds. In the above code snippet, the screen would never let the user scroll beneath 0.0 or above 1.0.v

## Integrating with your screen-enabled application
Fruity Menu does not "hog" the display and can therefore be combined with other applications to make full use of a screen. The key to integrating an application with Fruity Menu is controlling *who* renders to the screen and *when*.

For example, Fruity Menu was designed for the Adafruit RP2040 MacroPad. The "primary" application of the MacroPad was to execute hotkeys/keypress macros over USB. Fruity Menu provided an interface for users to configure their MacroPad.