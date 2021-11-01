import unittest

from fruity_menu.adjust import AdjustMenu, BoolMenu
from test.test_menu import HEIGHT, WIDTH

class AdjustMenuTests(unittest.TestCase):
    def test_getDisplayIo(self):
        menu = AdjustMenu('My label', HEIGHT, WIDTH)
        self.assertIsNone(menu.build_displayio_group(), 'Base class should have no implementation for building display')