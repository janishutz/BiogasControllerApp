import os
import configparser
from typing import override

config = configparser.ConfigParser()
config.read('./config.ini')

# Load config and disable kivy log if necessary
if config['Dev Settings']['verbose'] == "True":
    pass
else:
    os.environ["KIVY_NO_CONSOLELOG"] = "1"


# Load kivy modules
from kivy.core.window import Window, Config
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

# Load other libraries
import threading

# Store the current app version
app_version = f"{config['Info']['version']}{config['Info']['subVersion']}"

#---------#
# Screens #
#---------#

from gui.home.home import HomeScreen
from gui.credits.credits import CreditsScreen
from gui.settings.settings import SettingsScreen

#----------------#
# Screen Manager #
#----------------#
class BiogasControllerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()

    @override
    def build(self):
        self.icon = './BiogasControllerAppLogo.png'
        self.title = 'BiogasControllerApp-' + app_version
        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(CreditsScreen(name='credits'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        return self.screen_manager

if __name__ == "__main__":
    BiogasControllerApp().run()
