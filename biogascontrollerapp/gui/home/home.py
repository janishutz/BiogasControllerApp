from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from gui.popups.popups import QuitPopup, TwoActionPopup
from lib.com import ComSuperClass

import configparser


# This is the launch screen, i.e. what you see when you start up the app
class HomeScreen(Screen):
    def __init__(self, com: ComSuperClass, **kw):
        self._com = com;
        super().__init__(**kw)

    # Go to the main screen if we can establish connection or the check was disabled 
    # in the configs
    def start(self):
        if self._com.connect():
            self.manager.current = 'main'
            self.manager.transition.direction = 'right'
        else:
            TwoActionPopup().open('Failed to connect', 'Details', self.open_details_popup)
            print('ERROR connecting')

    # Open popup for details as to why the connection failed
    def open_details_popup(self):
        # TODO: Finish
        print( 'Details' )

    # Helper to open a Popup to ask user whether to quit or not
    def quit(self):
        QuitPopup(self._com).open()

    # Switch to about screen
    def to_about(self):
        self.manager.current = 'about'
        self.manager.transition.direction = 'down'


# Load the design file for this screen (.kv files)
# The path has to be relative to root of the app, i.e. where the biogascontrollerapp.py 
# file is located
Builder.load_file('./gui/home/home.kv')
