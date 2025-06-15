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

# Load the config file
import configparser
import time
config = configparser.ConfigParser()
config.read("./config.ini")


# Introducing tariffs to Python imports.
# It was too funny of an idea to miss out on
# You can enable or disable this in the config. 
# It is disabled by default
if config["Tariffs"]["impose_tariffs"] == "True":
    try:
        import tariff

        tariff.set({
            "kivy": int(config["Tariffs"]["kivy_rate"]),
            "serial": int(config["Tariffs"]["pyserial_rate"]),
            })
    except Exception as e:
        print(e)
        print("You cannot evade the tariffs. I will impose impose a tariff of 1000000% on the launch of this app!")
        time.sleep(2000000)

import os
from typing import override

from lib.com import Com, ComSuperClass
import lib.test.com



# Load config and disable kivy log if necessary
if config["Dev"]["verbose"] == "True":
    pass
else:
    os.environ["KIVY_NO_CONSOLELOG"] = "1"


# Load kivy modules. Kivy is the UI framework used. See https://kivy.org
# from kivy.core.window import Window, Config
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp


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
class BiogasControllerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()

    @override
    def build(self):
        com: ComSuperClass = Com()
        if config["Dev"]["use_test_library"] == "True":
            com = lib.test.com.Com()

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "Lime"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8

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
    print("""
┏━━┓━━━━━━━━━━━━━━━━━━━━┏━━━┓━━━━━━━━━┏┓━━━━━━━━┏┓━┏┓━━━━━━━━┏━━━┓━━━━━━━━
┃┏┓┃━━━━━━━━━━━━━━━━━━━━┃┏━┓┃━━━━━━━━┏┛┗┓━━━━━━━┃┃━┃┃━━━━━━━━┃┏━┓┃━━━━━━━━
┃┗┛┗┓┏┓┏━━┓┏━━┓┏━━┓━┏━━┓┃┃━┗┛┏━━┓┏━┓━┗┓┏┛┏━┓┏━━┓┃┃━┃┃━┏━━┓┏━┓┃┃━┃┃┏━━┓┏━━┓
┃┏━┓┃┣┫┃┏┓┃┃┏┓┃┗━┓┃━┃━━┫┃┃━┏┓┃┏┓┃┃┏┓┓━┃┃━┃┏┛┃┏┓┃┃┃━┃┃━┃┏┓┃┃┏┛┃┗━┛┃┃┏┓┃┃┏┓┃
┃┗━┛┃┃┃┃┗┛┃┃┗┛┃┃┗┛┗┓┣━━┃┃┗━┛┃┃┗┛┃┃┃┃┃━┃┗┓┃┃━┃┗┛┃┃┗┓┃┗┓┃┃━┫┃┃━┃┏━┓┃┃┗┛┃┃┗┛┃
┗━━━┛┗┛┗━━┛┗━┓┃┗━━━┛┗━━┛┗━━━┛┗━━┛┗┛┗┛━┗━┛┗┛━┗━━┛┗━┛┗━┛┗━━┛┗┛━┗┛━┗┛┃┏━┛┃┏━┛
━━━━━━━━━━━┏━┛┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃┃━━┃┃━━
━━━━━━━━━━━┗━━┛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┗┛━━┗┛━━

                            Version 3.0.0

 => Initializing....
          """)
    BiogasControllerApp().run()
    print("\n => Exiting!")
