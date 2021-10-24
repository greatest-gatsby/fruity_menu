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

class MenuOption:
    text = ''
    submenu = None
    upmenu = None

    def __init__(self, title: str):
        self.text = title

class Menu:
    """
    Boolean which tells whether the menu is currently Opened
    """
    _is_active = False

    """
    The Display object instatiated from your driver/main. Used to access the display and controls.
    """
    _display: Display = None

    """
    The 0-based index of the currently selected item
    """
    _selection = 0

    _options = []

    def __init__(self, display: Display, show_menu_title = True):
        self._display = display

    def add_action_button(self, title: str):
        act = ActionButton(title)
        act.upmenu = self
        self._options.append(act)
        return act

    def add_submenu_button(self, title: str):
        sub = SubmenuButton(title)
        sub.upmenu = self
        self._options.append(sub)
        return sub

    def add_value_button(self, title: str):
        val = ValueButton(title)
        val.upmenu = self
        self._options.append(val)
        return val

    def get_options_as_group(self):
        for opt in self._options:
            # calculate position
            pass
    

    def show_menu(self):
        menu_label = label.Label(terminalio.FONT, text='   MENU', color=OPT_HIGHLIGHT_TEXT_COLOR, background_color=OPT_HIGHLIGHT_BACK_COLOR)
        menu_label.x = 0
        menu_label.y = 10

        pages_color = OPT_TEXT_COLOR
        pages_back_color = OPT_BACK_COLOR
        if (self._selection == 0):
            pages_color = OPT_HIGHLIGHT_TEXT_COLOR
            pages_back_color = OPT_HIGHLIGHT_BACK_COLOR

        pages_label = label.Label(terminalio.FONT, text='Pages...', color=pages_color, background_color=pages_back_color, padding_left=OPT_PADDING)
        pages_label.x = 16
        pages_label.y = 24

        bright_color = OPT_TEXT_COLOR
        bright_back_color = OPT_BACK_COLOR
        if (self._selection == 1):
            bright_color = OPT_HIGHLIGHT_TEXT_COLOR
            bright_back_color = OPT_HIGHLIGHT_BACK_COLOR
        
        brightness_label = label.Label(terminalio.FONT, text='Brightness...', color=bright_color, background_color=bright_back_color, padding_left=OPT_PADDING)
        brightness_label.x = 16
        brightness_label.y = 40

        navback_color = OPT_TEXT_COLOR
        navback_back_color = OPT_BACK_COLOR
        if (self._selection == 2):
            navback_color = OPT_HIGHLIGHT_TEXT_COLOR
            navback_back_color = OPT_HIGHLIGHT_BACK_COLOR
        
        navback_label = label.Label(terminalio.FONT, text='<- Back', color=navback_color, background_color=navback_back_color, padding_left=OPT_PADDING)
        navback_label.x = 16
        navback_label.y = 56

        grp = Group()
        grp.append(menu_label)
        grp.append(pages_label)
        grp.append(brightness_label)
        grp.append(navback_label)

        self._display.display.show(grp)
        self._is_active = True
        return


    def show_main(self):
        #self._lines = self._display.display_text(title='Macpad')
        #self._lines.show()
        self._is_active = False
        pass

    def toggle_menu(self):
        if (self._is_active):
            if (self._selection == 2):
                self.show_main()
                return False
            else:
                # execute the currently active option
                return True
        else:
            self.show_menu()
            return True

    def scroll(self, delta: int):
        if delta > 0:
            if self._selection == OPTIONS - 1:
                self._selection = 0
            else:
                self._selection = self._selection + 1
        if delta < 0:
            if self._selection == 0:
                self._selection = OPTIONS - 1
            else:
                self._selection = self._selection - 1
        print('Scrolled to', self._selection, 'using delta', delta)
        return self._selection


class ActionButton(MenuOption):
    action = None

class SubmenuButton(MenuOption):
    submenu: Menu = None
    pass

class ValueButton(MenuOption):
    target = None
    pass