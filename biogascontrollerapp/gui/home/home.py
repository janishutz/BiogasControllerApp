from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from gui.popups.popups import QuitPopup, SingleRowPopup, TwoActionPopup
from lib.com import Com

class HomeScreen(Screen):
    def __init__(self, com: Com, **kw):
        self._com = com;
        super().__init__(**kw)

    def start(self):
        if self._com.connect(19200):
            self.manager.current = 'main'
            self.manager.transition.direction = 'right'
        else:
            TwoActionPopup().open('Failed to connect', 'Details', self.open_details_popup)
            print('ERROR connecting')

    def open_details_popup(self):
        print( 'Details' )

    def quit(self):
        QuitPopup(self._com).open()

    def to_about(self):
        self.manager.current = 'about'
        self.manager.transition.direction = 'down'


Builder.load_file('./gui/home/home.kv')
