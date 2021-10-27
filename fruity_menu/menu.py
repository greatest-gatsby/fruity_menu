from math import trunc
from displayio import Display, Group
import terminalio
from adafruit_display_text import label

OPTIONS = 3
OPT_HIGHLIGHT_TEXT_COLOR = 0x0000FF
OPT_HIGHLIGHT_BACK_COLOR = 0xFFAA00
OPT_TEXT_COLOR = 0xFFAA00
OPT_BACK_COLOR = 0x0000FF
OPT_PADDING = 24
PX_PER_LINE = 16
INITIAL_Y = 8

class MenuOption:
    """
    Building block of all options a menu can display.
    """
    text = ''
    upmenu = None

    def __init__(self, title: str):
        self.text = title

    def click(self):
        print('Click:',self.text)
        return True

class Menu:
    """
    The main class for building a menu. This is what most library users should be instatiating.

    Add submenus and menu options using instance methods.

    Render the menu by passing the resulting `displayio.Group` to the display of your choosing.
    """
    
    _is_active = False
    """
    Boolean which tells whether the menu is currently Opened
    """
    
    _display: Display = None
    """
    The Display object instatiated from your driver/main. Used to access the display and controls.
    """
    
    _selection = 0
    """
    The 0-based index of the currently selected item
    """

    _options = []
    """
    List of menu items
    """

    _activated_submenu = None
    """
    The currently opened submenu, if any
    """
    
    _title: str = 'Menu'
    """
    Title for this menu
    """
   
    _show_title = True
    """
    Whether to show Title at the top of the menu
    """

    _x = 4
    """
    X-coordinate for rendering menu
    """

    _y = INITIAL_Y
    """
    Y-coordinate for rendering menu
    """

    def __init__(self, display: Display, show_menu_title = True, title: str = 'Menu'):
        """
        Create a Menu for the given display.
        """
        self._display = display
        self._title = title
        self._show_title = show_menu_title
        self._options = []

    def add_action_button(self, title: str, action):
        """Add a button to this menu that invokes the given function when clicked."""
        act = ActionButton(title, action)
        act.upmenu = self
        self._options.append(act)
        return act

    def add_submenu_button(self, title: str, sub, add_upmenu_btn = '<- Back'):
        """
        Add a button to this menu that opens the given submenu when clicked.

        If a string is provided for `add_upmenu_btn`, the submenu will get an exit button
        which navigates up a level to this parent menu. The string will be used as the button's label.
        """
        menubut = SubmenuButton(title, sub)
        if (add_upmenu_btn != '' and add_upmenu_btn != None):
            sub.add_action_button(add_upmenu_btn, self._submenu_is_closing)

        #menubut.upmenu = self
        #menubut.submenu = sub
        self._options.append(menubut)
        return menubut

    def add_value_button(self, title: str, value):
        """Add a button to this menu that lets users modify the value of the given variable"""
        val = ValueButton(title, value)
        val.upmenu = self
        self._options.append(val)
        return val

    def build_options_as_group(self):
        """Builds a `displayio.Group` of this menu and all its options and current selection."""
        self._y = INITIAL_Y
        grp = Group()
        if self._show_title:
            lbl = self.get_title_label()
            grp.append(lbl)
        
        for i in range(len(self._options)):
            opt = self._options[i]
            lbl = label.Label(terminalio.FONT)
            lbl.text = opt.text

            if self._selection == i:
                lbl.color = OPT_HIGHLIGHT_TEXT_COLOR
                lbl.background_color = OPT_HIGHLIGHT_BACK_COLOR
            else:
                lbl.color = OPT_TEXT_COLOR
                lbl.background_color = OPT_BACK_COLOR

            lbl.x = self._x
            lbl.y = self._y
            grp.append(lbl)

            self._y = self._y + PX_PER_LINE
        
        return grp


    def get_title_label(self):
        """Gets the Label for this menu's title and adjusts the builder's coordinates to compensate for the object"""
        lbl = label.Label(terminalio.FONT, text='    ' + self._title, color=OPT_HIGHLIGHT_TEXT_COLOR, background_color=OPT_HIGHLIGHT_BACK_COLOR)
        lbl.x = 0
        lbl.y = self._y

        self._y = self._y + PX_PER_LINE
        return lbl
    

    def show_menu(self):
        """Builds the option group and renders it to the display"""
        # if no submenu is open, then show this menu
        if self._activated_submenu is None:
            grp = self.build_options_as_group()
            self._display.show(grp)
            self._is_active = True
            return
        else:
            # if submenu active, then render that submenu
            return self._activated_submenu.show_menu()

    def click_selected(self):
        """Clicks the currently selected item and returns whether this menu is still open (True) or closed (False)"""
        selected = self._options[self._selection]
        return selected.click()

    def scroll(self, delta: int):
        """Update menu's selected position using the given delta and allowing circular scrolling. The menu is not graphically updated."""
        if delta > 0:
            # Loop to first item if scrolling down while on last item
            if self._selection == len(self._options) - 1:
                self._selection = 0
            # Else just scroll down
            else:
                self._selection = self._selection + 1
        if delta < 0:
            # Loop to last item if scrolling up while on first item
            if self._selection == 0:
                self._selection = len(self._options) - 1
            # Else just scroll up
            else:
                self._selection = self._selection - 1
        #print('Scrolled to', self._selection, 'using delta', delta)
        return self._selection
    
    def _submenu_is_closing(self):
        self._activated_submenu = None
        self.show_menu()


class ActionButton(MenuOption):
    """
    ActionButtons are used to invoke Python functions when the user clicks the button.
    For example, hooking the action to your menu's toggle function can work as an Exit button.
    """
    _action = None

    def __init__(self, text: str, action):
        """Creates an action button with the given title and that will execute the given action when clicked"""
        self._action = action
        super().__init__(text)

    def click(self):
        """Invoke this button's stored action"""
        super().click()
        return self._action()
        

class SubmenuButton(MenuOption):
    submenu: Menu = None

    def __init__(self, title: str, sub: Menu):
        self.submenu = sub
        super().__init__(title)

class ValueButton(MenuOption):
    target = None

    def __init__(self, title: str, value):
        self.target = value
        super().__init__(title)