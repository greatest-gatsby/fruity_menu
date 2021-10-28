import unittest

from adafruit_displayio_sh1106 import SH1106

from fruity_menu.abstract import AbstractMenuOption
from fruity_menu.options import ActionButton, SubmenuButton, ValueButton
from fruity_menu.menu import Menu



DISPLAY = SH1106
WIDTH = 128
HEIGHT = 32

def TRAP_ACTION():
    raise AssertionError('You should not have executed me!')

def PRINT_ACTION(arg1 = None, arg2 = None, arg3 = None, arg4 = None):
    print('you asked for it')
    if (arg1 is not None):
        print('\t',arg1)
    if (arg2 is not None):
        print('\t',arg2)
    if (arg3 is not None):
        print('\t',arg3)
    if (arg4 is not None):
        print('\t',arg4)

class MenuTests(unittest.TestCase):
    def test_constructor_requiresDisplay(self):
        menu = Menu(DISPLAY)

class MenuOptionTests(unittest.TestCase):
    menu = None

    def setUp(self):
        self.menu = Menu.without_display(WIDTH, HEIGHT)

    def test_menu_constructor_setsFields(self):
        menu_title = 'This is a title'
        menu_show_title = False
        menu = Menu(DISPLAY, show_menu_title=menu_show_title, title=menu_title)
        self.assertEqual(menu_show_title, menu._show_title)
        self.assertEqual(menu_title, menu._title)

    def test_menu_withoutDisplay_setsFields(self):
        menu_title = 'One more time'
        menu_show_title = True
        h = 16
        w = 16
        menu = Menu.without_display(h, w, menu_show_title, menu_title)
        
        self.assertEqual(menu_title, menu._title)
        self.assertEqual(menu_show_title, menu._show_title)
        self.assertEqual(h, menu._height)
        self.assertEqual(w, menu._width)

    def test_action_constructor_setsFields(self):
        btn_title = 'My title'
        act = ActionButton(btn_title, TRAP_ACTION)
        self.assertEqual(btn_title, act.text, 'Specified button title not set')
        self.assertEqual(TRAP_ACTION, act._action, 'Specified button action not set')

    def test_submenu_constructor_setsFields(self):
        btn_title = 'The subtitler'
        sub = SubmenuButton(btn_title, self.menu, PRINT_ACTION)
        self.assertEqual(btn_title, sub.text, 'Specified title not assigned to button')
        self.assertEqual(self.menu, sub.submenu, 'Specified menu not assigned to button')

    def test_value_constructor(self):
        btn_title = 'valyo'
        btn_val = 890
        val_btn = ValueButton(btn_title, btn_val, Menu(DISPLAY), PRINT_ACTION)
        self.assertEqual(btn_title, val_btn.text, 'Given title not assigned to button')
        self.assertEqual(btn_val, val_btn.target, 'Given value not assigned to button')


    def test_menuOption_constructor_setsFields(self):
        opt = AbstractMenuOption('My title')
        self.assertEqual(opt.text, 'My title')

    def test_addActionButton_setsFields(self):
        act = self.menu.add_action_button('Perform this', action=TRAP_ACTION)
        self.assertEqual(act.text, 'Perform this', 'Button text does not match string given to method')
        self.assertIn(act, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addSubmenuButton(self):
        somesubmenu = Menu(DISPLAY, title='Test menu')
        sub = self.menu.add_submenu_button('Title here', sub=somesubmenu)
        self.assertEqual(sub.text, 'Title here', 'Button text does not match string given to method')
        self.assertIn(sub, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addValueButton(self):
        someotherval = 123
        val = self.menu.add_value_button('More arg txt', someotherval)
        self.assertEqual(val.text, 'More arg txt', 'Given title not assigned to button')
        self.assertIn(val, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addSubmenu_useDiscreteOptionsLists(self):
        alt_sub = Menu(DISPLAY)
        self.menu.add_submenu_button('Alt menu', alt_sub)
        self.assertNotEqual(alt_sub._options, self.menu._options, 'Distinct child submenu references the same _options object as its parent')

    def test_addSubmenu_siblingsUseDiscreteOptionsLists(self):
        alt_sub = Menu(DISPLAY)
        self.menu.add_submenu_button('Alt menu', alt_sub)
        alt_sub.add_submenu_button('Going deeper', Menu(DISPLAY))

        dif_sub = Menu(DISPLAY)
        self.menu.add_submenu_button('Dif menu', dif_sub)

        self.assertNotEqual(alt_sub._options, dif_sub._options, 'Distinct submenu siblings reference the same _options object')

    def test_addSubmenu_addsExitButton(self):
        btn_text = 'GO UP'
        submenu = Menu(DISPLAY)
        og_len = len(submenu._options)
        
        self.menu.add_submenu_button('my btn', submenu, add_upmenu_btn=btn_text)
        new_len = len(submenu._options)
        self.assertNotEqual(og_len, new_len, 'NO Button was added to the submenu!')

        exit_btn = submenu._options[new_len - 1]
        self.assertEqual(btn_text, exit_btn.text, 'Added button text does not match expected')

        

class MenuBuildingTests(unittest.TestCase):
    def setUp(self):
        DISPLAY.height = 32
        DISPLAY.width = 128
        pass

    def test_buildGroup_menuWithTitle(self):
        menu = Menu(DISPLAY)
        anothermenu = Menu(DISPLAY)
        rando_valuo = 450
        act = menu.add_action_button('New action', action=TRAP_ACTION)
        sub = menu.add_submenu_button('Expand...', anothermenu)
        val = menu.add_value_button('Volume', rando_valuo)
        grp = menu.build_options_as_group()
        self.assertIn(act, menu._options)
        self.assertIn(sub, menu._options)
        self.assertIn(val, menu._options)
        # i have no faith in this test :)
        self.assertEqual(1, len(grp), 'Constructed group contains missing or unpected elements')

    def test_buildGroup_menuNoTitle(self):
        menu = Menu(DISPLAY, show_menu_title=False)
        menu.add_action_button('Accio test results', action=TRAP_ACTION)
        grp = menu.build_options_as_group()
        self.assertEqual(1, len(grp), 'Constructed group contains unexpected elements')