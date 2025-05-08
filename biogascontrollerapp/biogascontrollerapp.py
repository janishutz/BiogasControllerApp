# ────────────────────────────────────────────────────────────────────
#          ╭────────────────────────────────────────────────╮
#          │              BiogasControllerApp               │
#          ╰────────────────────────────────────────────────╯
#
# So you would like to read the source code? Nice!
# Just be warned, this application uses Thread and a UI Toolkit called 
# Kivy to run. If you are unsure of what functions do, consider 
# checking out the kivy docs at https://kivy.org/doc. 
# It also uses the pyserial library for communication with the micro-
# controller with RS232
#
# ────────────────────────────────────────────────────────────────────

import os
import configparser
from typing import override

from lib.com import Com


# Load the config file
config = configparser.ConfigParser()
config.read("./config.ini")

# Load config and disable kivy log if necessary
if config["Dev Settings"]["verbose"] == "True":
    pass
else:
    os.environ["KIVY_NO_CONSOLELOG"] = "1"


# Load kivy modules. Kivy is the UI framework used. See https://kivy.org
# from kivy.core.window import Window, Config
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App


# Store the current app version
app_version = f"{config['Info']['version']}{config['Info']['subVersion']}"


#          ╭────────────────────────────────────────────────╮
#          │                    Screens                     │
#          ╰────────────────────────────────────────────────╯
# Import all the screens (= pages) used in the app 
from gui.home.home import HomeScreen
from gui.credits.credits import CreditsScreen
from gui.program.program import ProgramScreen
from gui.about.about import AboutScreen
from gui.main.main import MainScreen



#          ╭────────────────────────────────────────────────╮
#          │                 Screen Manager                 │
#          ╰────────────────────────────────────────────────╯
# Kivy uses a screen manager to manage pages in the application
class BiogasControllerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()

    @override
    def build(self):
        com = Com()
        self.icon = "./BiogasControllerAppLogo.png"
        self.title = "BiogasControllerApp-" + app_version
        self.screen_manager.add_widget(HomeScreen(com, name="home"))
        self.screen_manager.add_widget(MainScreen(com, name="main"))
        self.screen_manager.add_widget(ProgramScreen(com, name="program"))
        self.screen_manager.add_widget(CreditsScreen(name="credits"))
        self.screen_manager.add_widget(AboutScreen(name="about"))
        return self.screen_manager


# Disallow this file to be imported
if __name__ == "__main__":
    BiogasControllerApp().run()
