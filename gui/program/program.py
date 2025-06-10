from typing import List
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from lib.decoder import Decoder
from lib.instructions import Instructions
from gui.popups.popups import SingleRowPopup, TwoActionPopup, empty_func
from lib.com import ComSuperClass
from kivy.clock import Clock


# The below list maps 0, 1, 2, 3 to a, b, c and t respectively
# This is used to set and read values of the UI
name_map = ["a", "b", "c", "t"]


class ProgramScreen(Screen):
    def __init__(self, com: ComSuperClass, **kw):
        self._com = com
        self._instructions = Instructions(com)
        self._decoder = Decoder()
        super().__init__(**kw)

    def load_config(self):
        Clock.schedule_once(self._load)

    # Load the current configuration from the micro-controller
    def _load(self, dt: float):
        # Hook to the microcontroller's data stream (i.e. sync up with it)
        if self._instructions.hook("RD", ["\n", "R", "D", "\n"]):
            config: List[List[str]] = []

            # Load config for all four sensors
            for _ in range(4):
                # Receive 28 bytes of data
                received = bytes()
                try:
                    received = self._com.receive(28)
                except:
                    # Open error popup
                    TwoActionPopup().open(
                        "Failed to connect to micro-controller, retry?",
                        "Cancel",
                        empty_func,
                        "Retry",
                        lambda: self._load(0),
                    )
                    return

                # Create a list of strings to store the config for the sensor
                # This list has the following elements: a, b, c, temperature
                config_sensor_i: List[str] = []

                # Create the list
                for j in range(4):
                    config_sensor_i.append(
                        str(self._decoder.decode_float(received[7 * j : 7 * j + 6]))
                    )

                # Add it to the config
                config.append(config_sensor_i)
        else:
            TwoActionPopup().open(
                "Failed to connect to micro-controller, retry?",
                "Cancel",
                empty_func,
                "Retry",
                lambda: self._load(0),
            )

    # Set the elements of the UI to the values of the config
    def _set_ui(self, config: List[List[str]]):
        for sensor_id in range(4):
            for property in range(4):
                self.ids[f"s{sensor_id + 1}_{name_map[property]}"].text = config[
                    sensor_id
                ][property]

    # Read values from the UI. Returns the values as a list or None if the check was infringed
    def _read_ui(self, enforce_none_empty: bool = True) -> List[float] | None:
        data: List[float] = []

        # Iterate over all sensor config input fields and collect the data
        for sensor_id in range(4):
            for property in range(4):
                value = self.ids[f"s{sensor_id + 1}_{name_map[property]}"].text

                # If requested (by setting enforce_none_empty to True, which is the default)
                # test if the cells are not empty and if we find an empty cell return None
                if enforce_none_empty and value == "":
                    return
                data.append(float(value))

        return data

    # Transmit the changed data to the micro-controller to reconfigure it
    def save(self):
        data = self._read_ui()
        if data == None:
            SingleRowPopup().open("Some fields are missing values!")
        else:
            try:
                self._instructions.change_config(data)
            except:
                SingleRowPopup().open("Could not save data!")
            SingleRowPopup().open("Data saved successfully")


# Load the design file for this screen (.kv files)
# The path has to be relative to root of the app, i.e. where the biogascontrollerapp.py
# file is located
Builder.load_file("./gui/program/program.kv")
