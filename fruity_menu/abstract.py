from displayio import Group

class AbstractMenu:

    _height: int = 32
    """The height in pixels of the constructed menus"""

    _width: int = 128
    """The width in pixels of the constructed menus"""

    def click(self):
        pass

    def scroll(self, delta: int):
        pass

    def show_menu(self):
        pass

    def build_displayio_group(self) -> Group:
        pass

class AbstractMenuOption:
    text: str = ''
    upmenu = None

    def __init__(self, text: str):
        self.text = text

    def click(self):
        pass