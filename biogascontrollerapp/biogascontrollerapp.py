import os
import configparser
from typing import override

from lib.com import Com

config = configparser.ConfigParser()
config.read('./config.ini')

# Load config and disable kivy log if necessary
if config['Dev Settings']['verbose'] == "True":
    pass
else:
    os.environ["KIVY_NO_CONSOLELOG"] = "1"


# Load kivy modules
# from kivy.core.window import Window, Config
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

# Load other libraries
# import threading

# Store the current app version
app_version = f"{config['Info']['version']}{config['Info']['subVersion']}"

#---------#
# Screens #
#---------#

from gui.home.home import HomeScreen
from gui.credits.credits import CreditsScreen
from gui.about.about import AboutScreen
from gui.main.main import MainScreen

#----------------#
# Screen Manager #
#----------------#
class BiogasControllerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()

    @override
    def build(self):
        com = Com();
        self.icon = './BiogasControllerAppLogo.png'
        self.title = 'BiogasControllerApp-' + app_version
        self.screen_manager.add_widget(HomeScreen(com, name='home'))
        self.screen_manager.add_widget(MainScreen(com, name='main'))
        self.screen_manager.add_widget(CreditsScreen(name='credits'))
        self.screen_manager.add_widget(AboutScreen(name='about'))
        return self.screen_manager

if __name__ == "__main__":
    BiogasControllerApp().run()
