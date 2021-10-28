from displayio import Group
from terminalio import FONT
from fruity_menu.abstract import AbstractMenu
import fruity_menu.menu

from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label

PADDING_V_PX = 1
PADDING_H_PX = 4

class AdjustMenu(AbstractMenu):
    label = ''
    property = None

    def __init__(self, label, height, width):
        self.label = label
        self._width = width
        self._height = height

    def get_display_io_group(self):
        pass


class BoolMenu(AdjustMenu):
    text_when_true = 'True'
    text_when_false = 'False'

    def __init__(self, property: bool, label, height, width, text_true = 'YEE', text_false = 'naw'):
        self.property = property
        self.label = label
        self._height = height
        self._width = width

    def get_displayio_group(self):
        grp = Group()
        title_label = self.get_title_label()
        grp.append(title_label)

        prop_text = Label(FONT)
        if (self.property):
            prop_text.text = self.text_when_true
        else:
            prop_text.text = self.text_when_false
        prop_text.anchor_point = (0.5, 0.5)
        prop_text.anchored_position = (self._width / 2, self._height / 2)
        grp.append(prop_text)

        print('Got BoolMenu Group')
        return grp

    def get_value(self):
        return property 

    def get_title_label(self):
        title = Label(FONT, padding_top=PADDING_V_PX, padding_bottom=PADDING_V_PX,padding_right=PADDING_H_PX,padding_left=PADDING_H_PX)
        title.text = self.label
        title.anchor_point = (0.5, 0)
        title.anchored_position = (self._width / 2, 0)
        
        title.color = 0x000000
        title.background_color = 0xffffff
        return title

    def click(self):
        print('BoolMenu CLICK')

    def scroll(self, delta):
        if delta % 2 == 1:
            self.property = not self.property