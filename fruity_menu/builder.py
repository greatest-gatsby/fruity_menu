from collections import OrderedDict

try:
    from typing import Union, TypeAlias, Callable
    TreeDictElement: TypeAlias = dict[str, Union["TreeElement",Callable, "Value"]]
    TreeListElement: TypeAlias = list[Tuple[str, Union["TreeElement",Callable, "Value"]]]
    TreeElement = Union[TreeDictElement, TreeListElement]
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
        
        
class Options:
    """
    This is a holder to keep the arguments to create an OptionMenu
    """
    def __init__(self, value, options, *, option_labels = None, on_value_set=None, on_set_args=None):
        self.value = value
        try:
            dct = OrderedDict(options)
        except ValueError:
            self.options = options
            self.option_labels = option_labels
        else:
            self.options = list(dct.values())
            self.option_labels = list(dct.keys())
        self.on_value_set = on_value_set
        self.on_set_args = on_set_args


class Action:
    """
    This is a holder to keep the arguments to create an ActionMenu
    """
    def __init__(self, function, *args):
        self.function = function
        self.args = args


def build_menu(menu: Menu, structure: TreeElement):
    if isinstance(structure, (list, tuple)):
        structure = OrderedDict(structure)
    for k, v in structure.items():
        if isinstance(v, (dict, list)):
            submenu = menu.create_menu(k)
            build_menu(submenu,v)
            menu.add_submenu_button(k, submenu)
        elif isinstance(v, Value):
            menu.add_value_button(k, **v.__dict__)
        elif isinstance(v, Options):
            menu.add_option_button(k, **v.__dict__)
        elif isinstance(v, Action):
            menu.add_action_button(k, v.function, v.args)
        elif callable(v):
            menu.add_action_button(k, v)
