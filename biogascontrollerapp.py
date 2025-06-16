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
import time
from lib.config import read_config, set_verbosity, str_to_bool

verbose = str_to_bool(read_config("Dev", "verbose", "False", type_to_validate="bool"))
verbose = verbose if verbose != None else False


# Introducing tariffs to Python imports.
# It was too funny of an idea to miss out on
# You can enable or disable this in the config.
# It is disabled by default
if str_to_bool(
    read_config("Tariffs", "impose_tariffs", "False", type_to_validate="bool")
):
    try:
        import tariff

        tariff.set(
            {
                "kivy": int(
                    read_config("Tariffs", "kivy_rate", "0", type_to_validate="int")
                ),
                "serial": int(
                    read_config("Tariffs", "pyserial_rate", "0", type_to_validate="int")
                ),
            }
        )
    except Exception as e:
        print(e)
        print(
            "You cannot evade the tariffs. I will impose impose a tariff of 1000000% on the launch of this app!"
        )
        time.sleep(2000000)

import os
from typing import override

from lib.com import Com, ComSuperClass
import lib.test.com


# Load config and disable kivy log if necessary
if verbose:
    pass
else:
    os.environ["KIVY_NO_CONSOLELOG"] = "1"


# Load kivy modules. Kivy is the UI framework used. See https://kivy.org
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp


# Set Window size
Window.size = (
    int(int(read_config("UI", "width", "800", type_to_validate="int"))),
    int(int(read_config("UI", "height", "600", type_to_validate="int"))),
)


#          ╭────────────────────────────────────────────────╮
#          │                    Screens                     │
#          ╰────────────────────────────────────────────────╯
# Import all the screens (= pages) used in the app
from gui.home.home import HomeScreen
from gui.program.program import ProgramScreen
from gui.about.about import AboutScreen
from gui.main.main import MainScreen


#          ╭────────────────────────────────────────────────╮
#          │                 Screen Manager                 │
#          ╰────────────────────────────────────────────────╯
# Kivy uses a screen manager to manage pages in the application
colors = [
    "Red",
    "Pink",
    "Purple",
    "DeepPurple",
    "Indigo",
    "Blue",
    "LightBlue",
    "Cyan",
    "Teal",
    "Green",
    "LightGreen",
    "Lime",
    "Yellow",
    "Amber",
    "Orange",
    "DeepOrange",
    "Brown",
    "Gray",
    "BlueGray",
]


class BiogasControllerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()

    @override
    def build(self):
        # Configure com
        filters = [
            x
            for x in read_config(
                "Connection",
                "filters",
                "USB-Serial Controller, Prolific USB-Serial Controller",
            ).split(",")
        ]

        baudrate = int(
            read_config("Connection", "baudrate", "19200", type_to_validate="int")
        )

        com: ComSuperClass = Com(
            baudrate,
            filters,
        )

        if str_to_bool(
            read_config("Dev", "use_test_library", "False", type_to_validate="bool")
        ):
            com = lib.test.com.Com(
                int(read_config("Dev", "fail_sim", "20", type_to_validate="int")),
                baudrate,
                filters,
            )
        com.set_port_override(read_config("Connection", "port_override", "None"))

        self.theme_cls.theme_style = read_config(
            "UI", "theme", "Dark", ["Dark", "Light"]
        )
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = read_config(
            "UI", "primary_color", "Green", colors
        )
        self.theme_cls.accent_palette = read_config(
            "UI", "accent_color", "Lime", colors
        )
        self.theme_cls.theme_style_switch_animation = False

        if verbose:
            print("\n", "-" * 20, "\n")

        self.icon = "./BiogasControllerAppLogo.png"
        self.title = "BiogasControllerApp-V3.1.0"
        self.screen_manager.add_widget(HomeScreen(com, name="home"))
        self.screen_manager.add_widget(MainScreen(com, name="main"))
        self.screen_manager.add_widget(ProgramScreen(com, name="program"))
        self.screen_manager.add_widget(AboutScreen(name="about"))
        return self.screen_manager

    def change_theme(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )


# Disallow this file to be imported
if __name__ == "__main__":
    print(
        """
┏━━┓━━━━━━━━━━━━━━━━━━━━┏━━━┓━━━━━━━━━┏┓━━━━━━━━┏┓━┏┓━━━━━━━━┏━━━┓━━━━━━━━
┃┏┓┃━━━━━━━━━━━━━━━━━━━━┃┏━┓┃━━━━━━━━┏┛┗┓━━━━━━━┃┃━┃┃━━━━━━━━┃┏━┓┃━━━━━━━━
┃┗┛┗┓┏┓┏━━┓┏━━┓┏━━┓━┏━━┓┃┃━┗┛┏━━┓┏━┓━┗┓┏┛┏━┓┏━━┓┃┃━┃┃━┏━━┓┏━┓┃┃━┃┃┏━━┓┏━━┓
┃┏━┓┃┣┫┃┏┓┃┃┏┓┃┗━┓┃━┃━━┫┃┃━┏┓┃┏┓┃┃┏┓┓━┃┃━┃┏┛┃┏┓┃┃┃━┃┃━┃┏┓┃┃┏┛┃┗━┛┃┃┏┓┃┃┏┓┃
┃┗━┛┃┃┃┃┗┛┃┃┗┛┃┃┗┛┗┓┣━━┃┃┗━┛┃┃┗┛┃┃┃┃┃━┃┗┓┃┃━┃┗┛┃┃┗┓┃┗┓┃┃━┫┃┃━┃┏━┓┃┃┗┛┃┃┗┛┃
┗━━━┛┗┛┗━━┛┗━┓┃┗━━━┛┗━━┛┗━━━┛┗━━┛┗┛┗┛━┗━┛┗┛━┗━━┛┗━┛┗━┛┗━━┛┗┛━┗┛━┗┛┃┏━┛┃┏━┛
━━━━━━━━━━━┏━┛┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃┃━━┃┃━━
━━━━━━━━━━━┗━━┛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┗┛━━┗┛━━

                            Version 3.1.0

 => Initializing....
          """
    )
    set_verbosity(verbose)
    BiogasControllerApp().run()
    print("\n => Exiting!")
