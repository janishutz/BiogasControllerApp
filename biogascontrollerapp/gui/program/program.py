from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


class HomeScreen(Screen):
    def start(self):
        pass

    def quit(self):
        pass

    def to_settings(self):
        pass


Builder.load_file('./gui/home/home.kv')
