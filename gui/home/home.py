from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from lib.com import ComSuperClass
import platform


# Information for errors encountered when using pyserial
information = {
    "Windows": {
        "2": "Un- and replug the cable and ensure you have the required driver(s) installed",
        "13": "You are probably missing a required driver or your cable doesn't work. Consult the wiki for more information",
        "NO_COM": "Could not find a microcontroller. Please ensure you have one connected and the required driver(s) installed",
    },
    "Linux": {
        "2": "Un- and replug the cable, or if you haven't plugged a controller in yet, do that",
        "13": "Incorrect permissions at /dev/ttyUSB0. Open a terminal and type: sudo chmod 777 /dev/ttyUSB0",
        "NO_COM": "Could not find a microcontroller. Please ensure you have one connected",
    },
}


# This is the launch screen, i.e. what you see when you start up the app
class HomeScreen(MDScreen):
    def __init__(self, com: ComSuperClass, **kw):
        self._com = com
        self.connection_error_dialog = MDDialog(
            title="Connection",
            text="Failed to connect. See Details for more information and troubleshooting guide",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda _: self.connection_error_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="Details", on_release=lambda _: self.open_details_popup()
                ),
            ],
        )

        self.quit_dialog = MDDialog(
            title="Exit BiogasControllerApp",
            text="Do you really want to exit BiogasControllerApp?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda _: self.quit_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="Quit", on_release=lambda _: self._quit()
                ),
            ],
        )
        super().__init__(**kw)

    def _quit(self):
        self._com.close()
        MDApp.get_running_app().stop()

    # Go to the main screen if we can establish connection or the check was disabled
    # in the configs
    def start(self):
        if self._com.connect():
            self.manager.current = "main"
            self.manager.transition.direction = "right"
        else:
            self.connection_error_dialog.open()
            print("[ COM ] Connection failed!")

    # Open popup for details as to why the connection failed
    def open_details_popup(self):
        self.connection_error_dialog.dismiss()
        self.details_dialog = MDDialog(
            title="Troubleshooting",
            text=self._generate_help(),
            buttons=[
                MDFlatButton(
                    text="Ok", on_release=lambda _: self.details_dialog.dismiss()
                )
            ],
        )
        self.details_dialog.open()

    def _generate_help(self) -> str:
        operating_system = platform.system()
        if operating_system == "Windows" or operating_system == "Linux":
            port = self._com.get_comport()
            if port == "Sim":
                return "Running in simulator, so this error is just simulated"

            information["Linux"][
                "13"
            ] = f"Incorrect permissions at {port}. Resolve by running 'sudo chmod 777 {port}'"


            if port == "":
                return information[operating_system]["NO_COM"]

            err = self._com.get_error()
            if err != None:
                return information[operating_system][str(err.errno)]
            else:
                return "No error message available"
        else:
            return (
                "You are running on an unsupported Operating System. No help available"
            )

    # Helper to open a Popup to ask user whether to quit or not
    def quit(self):
        self.quit_dialog.open()

    # Switch to about screen
    def to_about(self):
        self.manager.current = "about"
        self.manager.transition.direction = "down"


# Load the design file for this screen (.kv files)
# The path has to be relative to root of the app, i.e. where the biogascontrollerapp.py
# file is located
Builder.load_file("./gui/home/home.kv")
