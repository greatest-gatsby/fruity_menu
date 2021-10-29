import unittest

from fruity_menu.adjust import BoolMenu
from test.test_menu import DISPLAY, HEIGHT, WIDTH

HEIGHT = 64
WIDTH = 128

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
        self.b_menu = BoolMenu(self.b_prop, self.b_text, HEIGHT, WIDTH)
        return super().setUp()

    def test_titleLabel(self):
        grp = self.b_menu.get_title_label()
        pass