import unittest
from unittest.mock import Mock
from fruity_menu.adjust import AdjustMenu
from fruity_menu.menu import Menu
from fruity_menu.options import ActionButton, SubmenuButton as Subbut, ValueButton as Valbut

def empty_action():
    pass

class ActionButtonTests(unittest.TestCase):
    button: ActionButton = None
    text: str = 'My Label'

    def setUp(self) -> None:
        self.button = ActionButton(self.text, empty_action)
        return super().setUp()

    def test_click_invokesActionWithArgs(self):
        self.button._args = Mock()
        self.button._action = Mock()
        result = self.button.click()

        self.button._action.assert_called_once_with(self.button._args)
        self.assertTrue(result)

    def test_click_invokesActionWithoutArgs(self):
        self.button._args = None
        self.button._action = Mock()
        result = self.button.click()
        self.button._action.assert_called_once_with()
        self.assertTrue(result)

class SubmenuButton(unittest.TestCase):
    button: Subbut = None
    submenu: Menu = None
    text: str = 'My Label Two'

    action = Mock()

    def setUp(self) -> None:
        self.submenu = Mock()
        self.button = Subbut(self.text, self.submenu, self.action)

    def test_click_invokesAction(self):
        result = self.button.click()
        self.action.assert_called_once_with(self.submenu)
        self.assertIsNone(result)

class ValueButton(unittest.TestCase):
    button: Valbut = None
    value: int = 38
    text: str = 'My Label three'
    value_menu: AdjustMenu = None
    action = None

    def setUp(self) -> None:
        self.button = Valbut(self.text, self.value, self.value_menu, self.action)

    def test_click_invokesAction(self):
        self.button._notify_parent = Mock()
        result = self.button.click()
        self.button._notify_parent.assert_called_once_with(self.value_menu)
        self.assertIsNone(result)