import unittest
from unittest.mock import Mock
from fruity_menu.adjust import BoolMenu

from test.test_menu import HEIGHT, WIDTH


class BoolMenuTests(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_constructor_setsFields(self):
        selected_value = True
        text = 'This is a news show'
        bm = BoolMenu(selected_value, text, HEIGHT, WIDTH)

        self.assertEqual(selected_value, bm.property)
        self.assertEqual(text, bm.label)
        self.assertEqual(HEIGHT, bm._height)
        self.assertEqual(WIDTH, bm._width)


class BoolMenuBuilderTests(unittest.TestCase):
    b_menu = None
    b_prop = True
    b_text = 'Turbo Mode'

    def setUp(self) -> None:
        self.b_prop = True
        self.b_text = 'Turbo Mode'
        self.b_menu = BoolMenu(self.b_prop, self.b_text, HEIGHT, WIDTH)
        return super().setUp()

    def test_titleLabel(self):
        lbl = self.b_menu.get_title_label()
        self.assertIsNotNone(lbl, 'Function should have returned an Adafruit text Label')
        self.assertEqual(self.b_text, lbl.text, 'Label text does not match the string that should have been used')

    def test_getDisplayIoGroup(self):
        grp = self.b_menu.build_displayio_group()
        self.assertIsNotNone(grp, 'Function should have returned a `displayio.Group`')
        self.assertEqual(2, len(grp), 'Function should have had exactly two layers: value and label')

    def test_getDisplayIoGroup_usesTrueText(self):
        plant_text = 'The Incredible True Story'
        plant_bad_text = 'If you click u lose'
        self.b_menu.text_when_false = plant_bad_text
        self.b_menu.text_when_true = plant_text
        grp = self.b_menu.build_displayio_group()
        self.assertEqual(self.b_text, grp[0].text, 'Group should start with the menu title')
        self.assertNotEqual(plant_bad_text, grp[1].text, 'Function used the text for False values, but this value is True')
        self.assertEqual(plant_text, grp[1].text, 'Group should end with the text for True values')

    def test_getDisplayIoGroup_usesFalseText(self):
        plant_text = 'The Incredible True Story'
        plant_bad_text = 'If you click u lose'
        self.b_prop = False
        self.b_menu = BoolMenu(self.b_prop, self.b_text, HEIGHT, WIDTH)
        self.b_menu.text_when_false = plant_text
        self.b_menu.text_when_true = plant_bad_text
        grp = self.b_menu.build_displayio_group()
        self.assertEqual(self.b_text, grp[0].text, 'Group should start with the menu title')
        self.assertNotEqual(plant_bad_text, grp[1].text, 'Function used the text for True values, but this value is False')
        self.assertEqual(plant_text, grp[1].text, 'Group should end with the text for False values')

    def test_click_invokesStoredAction_withArgs(self):
        self.b_menu.on_value_set = Mock()
        self.b_menu.on_value_set_args = Mock()
        click_value = self.b_menu.click()
        self.b_menu.on_value_set.assert_called_once_with(self.b_menu.on_value_set_args, self.b_prop)
        self.assertFalse(click_value)

    def test_click_invokesStoredAction_withoutArgs(self):
        self.b_menu.on_value_set = Mock()
        self.b_menu.on_value_set_args = None
        click_value = self.b_menu.click()
        self.b_menu.on_value_set.assert_called_once_with(self.b_prop)
        self.assertFalse(click_value)

    def test_click_justReturnIfNoStoredAction(self):
        self.b_menu.on_value_set = None
        self.assertFalse(self.b_menu.click())

    def test_scroll_oddDeltasflipValue(self):
        self.b_menu.scroll(131)
        self.assertFalse(self.b_menu.property)

    def test_scroll_evenDeltasNoChange(self):
        self.b_menu.scroll(821214)
        self.assertTrue(self.b_menu.property)
