from kivy.uix.popup import Popup
from kivy.lang import Builder


class ThisPopup(Popup):
    def start(self):
        pass

    def quit(self):
        pass

    def to_settings(self):
        pass


Builder.load_file('./gui/home/home.kv')
