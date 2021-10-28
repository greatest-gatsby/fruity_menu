from math import ceil, floor
from displayio import Display, Group
import terminalio
from adafruit_display_text import label


OPTIONS = 3
OPT_HIGHLIGHT_TEXT_COLOR = 0x0000FF
OPT_HIGHLIGHT_BACK_COLOR = 0xFFAA00
OPT_TEXT_COLOR = 0xFFAA00
OPT_BACK_COLOR = 0x0000FF
OPT_PADDING = 24
PX_PER_LINE = 14
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

    _width = 128
    """The width in pixels of the constructed menus"""
    
    _height = 32
    """The height in pixels of the constructed menus"""

    def __init__(self, display: Display, show_menu_title = True, title: str = 'Menu'):
        """
        Create a Menu for the given display.
        """
        self._display = display
        if (self._display is not None):
            self._width = display.width
            self._height = display.height
        self._title = title
        self._show_title = show_menu_title
        self._options = []

    def without_display(height: int, width: int, show_menu_title = True, title: str = 'Menu'):
        """
        Create a Menu with the given width and height in pixels.
        """
        menu = Menu(None, show_menu_title, title)
        menu._width = width
        menu._height = height
        return menu

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
        menubut = SubmenuButton(title, sub, self._submenu_is_opening)
        if (add_upmenu_btn != '' and add_upmenu_btn != None):
            sub.add_action_button(add_upmenu_btn, self._submenu_is_closing)
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

        # determine number of rows to fit on-screen
        remaining_y_px = self._display.height - self._y
        max_rows_per_page = floor(remaining_y_px / PX_PER_LINE)
        
        # determine the indices of the page and row for paginated display
        if (self._selection == 0):
            selected_relative_row = 0
            selected_page = 0
        else:
            selected_relative_row = self._selection % max_rows_per_page
            selected_page = floor(self._selection / max_rows_per_page)
        
        index_offset = selected_page * max_rows_per_page        

        for i in range(max_rows_per_page):
            if (i + index_offset >= len(self._options)):
                continue
            opt = self._options[i + index_offset]
            lbl = label.Label(terminalio.FONT)
            lbl.text = opt.text

            if i == selected_relative_row:
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
        """
        Builds the option group and renders it to the display.

        If this Menu was built without a Display object, then this function
        will return the `displayio.Group` that needs to be shown on the display.

        If this Menu was built WITH a Display object, then this function
        will instead display the `Group` itself and return nothing.
        """
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
        # Exec submenu if open
        if (self._activated_submenu != None):
            return self._activated_submenu.click_selected()
        
        # otherwise click this menu
        selected = self._options[self._selection]
        return selected.click()
            

    def scroll(self, delta: int):
        """Update menu's selected position using the given delta and allowing circular scrolling. The menu is not graphically updated."""
        # Exec submenu if open
        if (self._activated_submenu != None):
            return self._activated_submenu.scroll(delta)
        
        # Else, scroll this menu
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

    def _submenu_is_opening(self, activated_menu):
        self._activated_submenu = activated_menu



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
    """
    SubmenuButtons open nested Menus when clicked.
    """
    submenu: Menu = None
    _notify_parent = None

    def __init__(self, title: str, sub: Menu, on_open):
        self.submenu = sub
        self._notify_parent = on_open
        super().__init__(title)

    def click(self):
        super().click()
        print('Opening submenu...')
        self._notify_parent(self.submenu)
        self.submenu.show_menu()

class ValueButton(MenuOption):
    """
    ValueButtons let users modify property values.
    Only some types are supported.
    """
    target = None

    def __init__(self, title: str, value):
        self.target = value
        super().__init__(title)