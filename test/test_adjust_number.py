import unittest
from unittest.mock import Mock
from fruity_menu.adjust import NumberMenu

from test.test_menu import HEIGHT, WIDTH

class NumberMenuTests(unittest.TestCase):
    n_menu: NumberMenu = None
    title: str = 'The Title'
    value = 856

    def setUp(self) -> None:
        self.n_menu = NumberMenu(self.value, self.title, HEIGHT, WIDTH)
        return super().setUp()

    def test_getDisplayIoGroup(self):
        grp = self.n_menu.build_displayio_group()
        self.assertEqual(self.title, grp[0].text)
        self.assertEqual(str(self.value), grp[1].text)
        self.assertEqual(2, len(grp), 'Group contains unexpected elements')

    def test_click_invokesStoredAction_withArgs(self):
        self.n_menu.on_value_set = Mock()
        self.n_menu.on_value_set_args = Mock()
        click_value = self.n_menu.click()
        self.n_menu.on_value_set.assert_called_once_with(self.n_menu.on_value_set_args, self.value)
        self.assertFalse(click_value)

    def test_click_invokesStoredAction_withoutArgs(self):
        self.n_menu.on_value_set = Mock()
        self.n_menu.on_value_set_args  = None
        click_value = self.n_menu.click()
        self.n_menu.on_value_set.assert_called_once_with(self.value)
        self.assertFalse(click_value)

    def test_click_justReturnIfNoStoredAction(self):
        self.n_menu.on_value_set = None
        self.assertFalse(self.n_menu.click())

    def test_scroll_propertyIncrementsWithFactor(self):
        scroll_factor = 4
        scroll_delta = 6
        starting = self.n_menu.property
        self.n_menu.scroll_factor = scroll_factor
        self.n_menu.scroll(scroll_delta)
        self.assertEqual((scroll_delta * scroll_factor) + starting, self.n_menu.property)

    