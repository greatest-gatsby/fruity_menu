import unittest
from unittest.mock import Mock
from fruity_menu.adjust import ArrayMenu

from test.test_menu import HEIGHT, WIDTH


class ArrayMenuTests(unittest.TestCase):
    title: str = 'The Title'
    list_options = [10, 20, 30, 60]
    labels = ['A', 'B', 'C', 'D']

    def test_getDisplayIoGroup(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)
        grp = self.a_menu.build_displayio_group()
        self.assertEqual(self.title, grp[0].text)
        self.assertEqual(str(10), grp[1].text)
        self.assertEqual(2, len(grp), 'Group contains unexpected elements')

    def test_getDisplayIoGroup_with_labels(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH,
                                option_labels=self.labels)
        grp = self.a_menu.build_displayio_group()
        self.assertEqual(self.title, grp[0].text)
        self.assertEqual(str(self.labels[0]), grp[1].text)
        self.assertEqual(2, len(grp), 'Group contains unexpected elements')

    def test_click_invokesStoredAction_withArgs(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)
        self.a_menu.on_value_set = Mock()
        self.a_menu.on_value_set_args = Mock()
        click_value = self.a_menu.click()
        self.a_menu.on_value_set.assert_called_once_with(self.a_menu.on_value_set_args, value)
        self.assertFalse(click_value)

    def test_click_invokesStoredAction_withoutArgs(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)
        self.a_menu.on_value_set = Mock()
        self.a_menu.on_value_set_args = None
        click_value = self.a_menu.click()
        self.a_menu.on_value_set.assert_called_once_with(value)
        self.assertFalse(click_value)

    def test_click_justReturnIfNoStoredAction(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)
        self.a_menu.on_value_set = None
        self.assertFalse(self.a_menu.click())

    def test_scroll_advances_correctly(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)
        self.a_menu.scroll(1)
        self.assertEqual(20, self.a_menu.property)

    def test_scroll_advances_correctly_with_labels(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH,
                                option_labels=self.labels)
        self.a_menu.scroll(1)
        self.assertEqual(20, self.a_menu.property)

    def test_scroll_wraps_on_increment(self):
        value = 60
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)
        self.a_menu.scroll(1)
        self.assertEqual(10, self.a_menu.property)

    def test_scroll_wraps_on_increment_with_labels(self):
        value = 60
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH,
                                option_labels=self.labels)
        self.a_menu.scroll(1)
        self.assertEqual(10, self.a_menu.property)

    def test_scroll_wraps_on_decrement(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)
        self.a_menu.scroll(-1)
        self.assertEqual(60, self.a_menu.property)

    def test_scroll_wraps_on_decrement_with_labels(self):
        value = 10
        self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH,
                                option_labels=self.labels)
        self.a_menu.scroll(-1)
        self.assertEqual(60, self.a_menu.property)

    def test_raises_error_if_value_not_in_options_list(self):
        value = 15
        with self.assertRaises(ValueError):
            self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH)

    def test_raises_error_if_value_not_in_options_dict(self):
        value = 15
        with self.assertRaises(ValueError):
            self.a_menu = ArrayMenu(value, self.list_options, self.title, HEIGHT, WIDTH,
                                    option_labels=self.labels)

    def test_raises_error_if_labels_list_different_length_to_options(self):
        with self.assertRaises(ValueError):
            self.a_menu = ArrayMenu(10, [10, 20, 30], self.title, HEIGHT, WIDTH,
                                    option_labels=["a", "b", "c", "d"])
