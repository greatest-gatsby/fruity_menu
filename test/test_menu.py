import unittest

from fruity_menu.menu import Menu, ActionButton, SubmenuButton, ValueButton, MenuOption
from adafruit_displayio_sh1106 import SH1106

class MenuTests(unittest.TestCase):
    def test_constructor_requiresDisplay(self):
        disp = SH1106
        menu = Menu(disp)

class MenuOptionTests(unittest.TestCase):
    menu = None
    disp = None

    def trap_action():
        raise AssertionError('You should not have executed me!')

    def setUp(self):
        self.disp = SH1106
        self.menu = Menu(self.disp)

    def test_action_constructor(self):
        act = ActionButton(self.menu, MenuOptionTests.trap_action)

    def test_submenu_constructor(self):
        sub = SubmenuButton('subtitle', self.menu)

    def test_value_constructor(self):
        val = ValueButton(self.menu)

    def test_menuOption_constructorSetsTitle(self):
        opt = MenuOption('My title')
        self.assertEqual(opt.text, 'My title')

    def test_addActionButton(self):
        act = self.menu.add_action_button('Perform this', action=MenuOptionTests.trap_action)
        self.assertEqual(act.text, 'Perform this', 'Button text does not match string given to method')
        self.assertIn(act, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addSubmenuButton(self):
        somesubmenu = Menu(SH1106, title='Test menu')
        sub = self.menu.add_submenu_button('Title here', sub=somesubmenu)
        self.assertEqual(sub.text, 'Title here', 'Button text does not match string given to method')
        self.assertIn(sub, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addValueButton(self):
        someotherval = 123
        val = self.menu.add_value_button('More arg txt')
        self.assertEqual(val.text, 'More arg txt')
        self.assertIn(val, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addSubmenus_useDiscreteOptionsLists(self):
        alt_sub = Menu(self.disp)
        self.menu.add_submenu_button('Alt menu', alt_sub)
        self.assertNotEqual(alt_sub._options, self.menu._options, 'Distinct child submenu references the same _options object as its parent')

    def test_addSubmenus_siblingsUseDiscreteOptionsLists(self):
        alt_sub = Menu(self.disp)
        self.menu.add_submenu_button('Alt menu', alt_sub)
        alt_sub.add_submenu_button('Going deeper', Menu(self.disp))

        dif_sub = Menu(self.disp)
        self.menu.add_submenu_button('Dif menu', dif_sub)

        self.assertNotEqual(alt_sub._options, dif_sub._options, 'Distinct submenu siblings reference the same _options object')


class MenuBuildingTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_buildGroup(self):
        menu = Menu(SH1106)
        anothermenu = Menu(SH1106)
        act = menu.add_action_button('New action', action=MenuOptionTests.trap_action)
        sub = menu.add_submenu_button('Expand...', anothermenu)
        val = menu.add_value_button('Volume')
        grp = menu.build_options_as_group()
        self.assertEqual(4, len(grp))
        self.assertIn(act, menu._options)
        self.assertIn(sub, menu._options)
        self.assertIn(val, menu._options)