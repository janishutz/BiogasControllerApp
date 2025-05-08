from typing import Callable
from kivy.uix.popup import Popup
from kivy.lang import Builder

from lib.com import Com


# Just an empty function
def empty_func():
    pass

#          ╭────────────────────────────────────────────────╮
#          │                     Popups                     │
#          ╰────────────────────────────────────────────────╯
# Below, you can find various popups with various designs that can be used in the app
class QuitPopup(Popup):
    def __init__(self, com: Com, **kw):
        self._com = com;
        super().__init__(**kw)

    def quit(self):
        self._com.close()

class SingleRowPopup(Popup):
    def open(self, message, *_args, **kwargs):
        self.ids.msg.text = message
        return super().open(*_args, **kwargs)

class DualRowPopup(Popup):
    def open(self, title: str, message: str, *_args, **kwargs):
        self.ids.msg_title.text = title
        self.ids.msg_body.text = message
        return super().open(*_args, **kwargs)

class LargeTrippleRowPopup(Popup):
    def open(self, title: str, message: str, details: str, *_args, **kwargs):
        self.ids.msg_title.text = title
        self.ids.msg_body.text = message
        self.ids.msg_extra.text = details
        return super().open(*_args, **kwargs)

class TwoActionPopup(Popup):
    def open(self, 
             message: str,
             button_one: str,
             action_one: Callable[[], None],
             button_two: str = 'Ok',
             action_two: Callable[[], None] = empty_func,
             *_args,
             **kwargs
        ):
        self.ids.msg.text = message
        self.ids.btn1.text = button_one
        self.ids.btn2.text = button_two
        self.action_one = action_one
        self.action_two = action_two
        return super().open(*_args, **kwargs)


# Load the design file for this screen (.kv files)
# The path has to be relative to root of the app, i.e. where the biogascontrollerapp.py 
# file is located
Builder.load_file('./gui/popups/popups.kv')
