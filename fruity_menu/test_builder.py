from unittest import TestCase
from unittest.mock import patch, Mock

import fruity_menu.menu
from fruity_menu.builder import build_menu, Value

def dummy_function():
    pass

@patch("fruity_menu.menu.Menu")
class TestBuilder(TestCase):

    def testActionAdd(self, Menu):
        menu: Mock = Menu()
        dct = {"test": dummy_function}
        build_menu(menu, dct)
        menu.add_action_button.assert_called_once_with("test", dummy_function)

    def testValueAddMinimal(self, Menu):
        i = 0
        menu: Mock = Menu()
        dct = {"test": Value(i, dummy_function)}
        build_menu(menu, dct)
        menu.add_value_button.assert_called_once_with("test",
                                                      value=i,
                                                      on_value_set= dummy_function,
                                                      on_set_args=None,
                                                      scroll_factor=1,
                                                      min_val=None,
                                                      max_val=None)

    def testValueAddMaximal(self, Menu):
        i = 0
        menu: Mock = Menu()
        dct = {"test": Value(i, on_value_set = dummy_function, on_set_args="set_args",
                             scroll_factor=2, min_val=-1, max_val=10)}
        build_menu(menu, dct)
        menu.add_value_button.assert_called_once_with("test",
                                                      value=i,
                                                      on_value_set= dummy_function,
                                                      on_set_args= "set_args",
                                                      scroll_factor=2,
                                                      min_val=-1,
                                                      max_val=10)

    def testSubMenuAdd(self, Menu):
        menu: Mock = Menu()
        sub_menu = Mock()
        menu.create_menu.return_value = sub_menu
        dct = {"sub_menu": {"test": dummy_function}}
        build_menu(menu, dct)
        menu.create_menu.assert_called_once_with("sub_menu")
        sub_menu.add_action_button.assert_called_once_with("test", dummy_function)
        menu.add_submenu_button.assert_called_once_with("sub_menu", sub_menu)

    def testSubMenuAddWithLists(self, Menu):
        menu: Mock = Menu()
        sub_menu = Mock()
        menu.create_menu.return_value = sub_menu
        dct = [("sub_menu", [("test", dummy_function)])]
        build_menu(menu, dct)
        menu.create_menu.assert_called_once_with("sub_menu")
        sub_menu.add_action_button.assert_called_once_with("test", dummy_function)
        menu.add_submenu_button.assert_called_once_with("sub_menu", sub_menu)
