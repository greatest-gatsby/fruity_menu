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
    text = ''
    submenu = None
    upmenu = None

    def __init__(self, title: str):
        self.text = title

    def click(self):
        print('Click:',self.text)

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

    """
    List of menu items
    """
    _options = []

    """
    Title for this menu
    """
    _title: str = 'Menu'

    """
    Whether to show Title at the top of the menu
    """
    _show_title = True

    """
    X-coordinate for rendering menu
    """
    _x = 4

    """
    Y-coordinate for rendering menu
    """
    _y = INITIAL_Y

    def __init__(self, display: Display, show_menu_title = True, title: str = 'Menu'):
        self._display = display
        self._title = title
        self._show_title = show_menu_title
        #print('Screen dimensions:', self._display.width, 'x', self._display.height)

    def add_action_button(self, title: str, action):
        act = ActionButton(title, action)
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

    def build_options_as_group(self):
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
        lbl = label.Label(terminalio.FONT, text='    ' + self._title, color=OPT_HIGHLIGHT_TEXT_COLOR, background_color=OPT_HIGHLIGHT_BACK_COLOR)
        lbl.x = 0
        lbl.y = self._y

        self._y = self._y + PX_PER_LINE
        return lbl
    

    def show_menu(self):
        grp = self.build_options_as_group()
        self._display.show(grp)
        self._is_active = True
        return

    def click_selected(self):
        selected = self._options[self._selection]
        return selected.click()

    def show_main(self):
        #self._lines = self._display.display_text(title='Macpad')
        #self._lines.show()
        self._is_active = False
        print('MAINAINAINAINAINAIN')
        pass

    def toggle_menu(self):
        if (self._is_active):
            self.show_main()
            return False
        else:
            self.show_menu()
            return True

    def scroll(self, delta: int):
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
        print('Scrolled to', self._selection, 'using delta', delta)
        return self._selection


class ActionButton(MenuOption):
    _action = None

    def __init__(self, text: str, action):
        super().__init__(text)
        self._action = action

    def click(self):
        super().click()
        print('Child click')
        return self._action()
        

class SubmenuButton(MenuOption):
    submenu: Menu = None
    pass

class ValueButton(MenuOption):
    target = None
    pass