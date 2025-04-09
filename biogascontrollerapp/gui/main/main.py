from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from lib.com import Com


class MainScreen(Screen):
    def __init__(self, com: Com, **kw):
        self._com = com;
        super().__init__(**kw)

    def start(self):
        pass

    def end(self):
        pass

    def reset(self):
        pass

    def back(self):
        pass


Builder.load_file('./gui/main/main.kv')
