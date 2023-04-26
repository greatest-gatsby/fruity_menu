try:
    from typing import Union, TypeAlias, Callable
    TreeElement: TypeAlias = dict[str, Union["TreeElement",Callable, "Value"]]
except ImportError:
    TreeElement = dict
from fruity_menu.menu import Menu


class Value:
    """
    This is a holder to keep the arguments to create a ValueButton
    """
    def __init__(self, value, on_value_set = None, on_set_args = None,
                         scroll_factor = 1, min_val = None, max_val = None):
        self.value = value
        self.on_value_set = on_value_set
        self.on_set_args = on_set_args
        self.scroll_factor = scroll_factor
        self.min_val = min_val
        self.max_val = max_val


def build_menu(menu: Menu, structure: TreeElement):
    for k, v in structure.items():
        if isinstance(v, dict):
            submenu = menu.create_menu(k)
            build_menu(submenu,v)
            menu.add_submenu_button(k, submenu)
        elif isinstance(v, Value):
            menu.add_value_button(k, **v.__dict__)
        elif callable(v):
            menu.add_action_button(k, v)
