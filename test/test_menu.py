import unittest

from fruity_menu.menu import Menu, ActionButton, SubmenuButton, ValueButton, MenuOption
from adafruit_displayio_sh1106 import SH1106

class MenuTests(unittest.TestCase):
    def test_constructor_requiresDisplay(self):
        disp = SH1106
        menu = Menu(disp)

class MenuOptionTests(unittest.TestCase):
    menu = None

    def setUp(self):
        self.menu = Menu(SH1106)

    def test_action_constructor(self):
        act = ActionButton(self.menu)

    def test_submenu_constructor(self):
        sub = SubmenuButton(self.menu)

    def test_value_constructor(self):
        val = ValueButton(self.menu)

    def test_menuOption_constructorSetsTitle(self):
        opt = MenuOption('My title')
        self.assertEqual(opt.text, 'My title')

    def test_addActionButton(self):
        act = self.menu.add_action_button('Perform this')
        self.assertEqual(act.text, 'Perform this', 'Button text does not match string given to method')
        self.assertIn(act, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addSubmenuButton(self):
        sub = self.menu.add_submenu_button('Title here')
        self.assertEqual(sub.text, 'Title here', 'Button text does not match string given to method')
        self.assertIn(sub, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addValueButton(self):
        val = self.menu.add_value_button('More arg txt')
        self.assertEqual(val.text, 'More arg txt')
        self.assertIn(val, self.menu._options, 'Button was returned but not added to its parent menu')

class MenuBuildingTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_buildGroup(self):
        menu = Menu(SH1106)
        act = menu.add_action_button('New action')
        sub = menu.add_submenu_button('Expand...')
        val = menu.add_value_button('Volume')
        grp = menu.build_options_as_group()
        self.assertEqual(4, len(grp))
        self.assertIn(act, menu._options)
        self.assertIn(sub, menu._options)
        self.assertIn(val, menu._options)