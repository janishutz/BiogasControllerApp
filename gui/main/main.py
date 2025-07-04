from ctypes import ArgumentError
from time import time
from typing import List, override
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock, ClockEvent
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import queue
import threading

# Load utilities
from util.instructions import Instructions
from util.interface import ControllerConnection
from util.decoder import Decoder


# TODO: Consider consolidating start and stop button


# Queue with data that is used to synchronize
synced_queue: queue.Queue[List[str]] = queue.Queue()


#          ╭────────────────────────────────────────────────╮
#          │           Data Reading Thread Helper           │
#          ╰────────────────────────────────────────────────╯
# Using a Thread to run this in parallel to the UI to improve responsiveness
class ReaderThread(threading.Thread):
    _com: ControllerConnection
    _decoder: Decoder
    _instructions: Instructions

    # This method allows the user to set Com object to be used.
    # The point of this is to allow for the use of a single Com object to not waste resources
    def set_com(self, com: ControllerConnection):
        """Set the Com object to be used in this

        Args:
            com: The com object to be used
        """
        self._com = com
        self._run = True
        self._decoder = Decoder()
        self._instructions = Instructions(com)

    # This method is given by the Thread class and has to be overriden to change
    # what is executed when the thread starts
    @override
    def run(self) -> None:
        self._run = True
        if self._com == None:
            raise ArgumentError("Com object not passed in (do using set_com)")
        # Hook to output stream
        if self._instructions.hook_main():
            # We are now hooked to the stream (i.e. data is synced)
            synced_queue.put(["HOOK", self._com.get_comport()])

            # making it exit using the stop function
            while self._run:
                # Take note of the time before reading the data to deduce frequency of updates
                start_time = time()

                # We need to read 68 bytes of data, given by the program running on the controller
                received = self._com.receive(68)

                # Store the data in a list of strings
                data: List[str] = []

                # For all sensors connected, execute the same thing
                for i in range(4):
                    # The slicing that happens here uses offsets automatically calculated from the sensor id
                    # This allows for short code
                    try:
                        data.append(
                            f"Tadc: {
                                self._decoder.decode_int(received[12 * i:12 * i + 4])
                            }\nTemp: {
                                round(self._decoder.decode_float(received[12 * i + 5:12 * i + 11]) * 1000) / 1000
                            }°C\nDC: {
                                round((self._decoder.decode_float_long(received[48 + 5 * i: 52 + 5 * i]) / 65535.0 * 100) * 1000) / 1000
                            }%"
                        )
                    except:
                        data.append("Bad data")
                # Calculate the frequency of updates
                data.append(
                    str(round((1 / (time() - start_time)) * 1000) / 1000) + " Hz"
                )
                synced_queue.put(data)
        else:
            # Send error message to the UI updater
            synced_queue.put(["ERR_HOOK"])
            return

    def stop(self) -> None:
        self._run = False


#          ╭────────────────────────────────────────────────╮
#          │                Main App Screen                 │
#          ╰────────────────────────────────────────────────╯
# This is the main screen, where you can read out data
class MainScreen(MDScreen):
    _event: ClockEvent

    # The constructor if this class takes a Com object to share one between all screens
    # to preserve resources and make handling better
    def __init__(self, com: ControllerConnection, **kw):
        # Set some variables
        self._com = com
        self._event = None
        self._fast_mode = False

        # Set up Dialog for erros
        self.connection_error_dialog = MDDialog(
            title="Connection",
            text="Failed to connect. Do you wish to retry?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda _: self.connection_error_dialog.dismiss(),
                ),
                MDFlatButton(text="Retry", on_release=lambda _: self.start()),
            ],
        )

        self.mode_switch_error_dialog = MDDialog(
            title="Mode Switch",
            text="Failed to change mode. Please try again",
            buttons=[
                MDFlatButton(
                    text="Ok",
                    on_release=lambda _: self.mode_switch_error_dialog.dismiss(),
                ),
            ],
        )

        # Prepare the reader thread
        self._prepare_reader()
        self._has_run = False
        self._has_connected = False

        # Call the constructor for the Screen class
        super().__init__(**kw)

    def _prepare_reader(self):
        # Prepares the reader thread
        self._reader = ReaderThread()
        self._reader.daemon = True
        self._reader.set_com(self._com)

    # Small helper function that makes the UI not freeze by offloading
    def start(self):
        Clock.schedule_once(lambda _: self._start())

    # Start the connection to the micro-controller to read data from it.
    # This also starts the reader thread to continuously read out data
    def _start(self):
        # Prevent running multiple times
        self.connection_error_dialog.dismiss()
        if self._has_connected:
            return

        # Some UI config
        self.ids.status.text = "Connecting..."
        if self._com.connect():
            print("[ COM ] Connection Acquired")

            # Prevent multiple connections
            self._has_connected = True
            self._has_run = True
            if self._has_run:
                self._prepare_reader()

            # Start communication
            self._reader.start()
            print("[ COM ] Reader has started")

            # Schedule UI updates
            self._event = Clock.schedule_interval(self._update_screen, 0.5)
        else:
            self.ids.status.text = "Connection failed"
            self.connection_error_dialog.open()

    # End connection to micro-controller and set it back to normal mode
    def end(self, set_msg: bool = True):
        # Set micro-controller back to Normal Mode when ending communication
        # to make sure temperature control will work
        if self._has_connected:
            if self._event != None:
                self._event.cancel()
            self._reader.stop()

            # Join the thread to end it safely
            try:
                self._reader.join()
            except:
                pass

            # Go back to Normal Mode on the Controller
            # This is so you don't accidentally forget!
            try:
                self._com.send("NM")
            except:
                pass

            self._com.close()
            if set_msg:
                self.ids.status.text = "Connection terminated"
                self.ids.port.text = "Port: Not connected"
            self._has_connected = False
            print("Connection terminated")

    # A helper function to update the screen. Is called on an interval
    def _update_screen(self, _):
        update = []
        try:
            update = synced_queue.get_nowait()
        except:
            pass

        if len(update) == 0:
            # There are no updates to process, don't block and simply try again next time
            return

        if len(update) == 1:
            # Sync errors
            if update[0] == "ERR_HOOK":
                self.ids.status.text = "Hook failed"
                self.end(False)

        if len(update) == 2:
            # Connection successful
            if update[0] == "HOOK":
                self.ids.status.text = "Connected to controller"
                self.ids.port.text = "Port: " + update[1]
        else:
            # Update the UI
            self.ids.sensor1.text = update[0]
            self.ids.sensor2.text = update[1]
            self.ids.sensor3.text = update[2]
            self.ids.sensor4.text = update[3]
            self.ids.status.text = "Connected, f = " + update[4]

    # Reset the screen when the screen is entered
    def reset(self):
        self.ids.sensor1.text = ""
        self.ids.sensor2.text = ""
        self.ids.sensor3.text = ""
        self.ids.sensor4.text = ""
        self.ids.status.text = "Status will appear here"
        self.ids.port.text = "Port: Not connected"

    # Switch the mode for the micro-controller
    def switch_mode(self):
        # Store if we have been connected to the micro-controller before mode was switched
        was_connected = self._has_connected

        # Disconnect from the micro-controller
        self.end()
        self.ids.status.text = "Setting mode..."

        # Try to set the new mode
        try:
            if self._fast_mode:
                self._com.send("NM")
            else:
                self._com.send("FM")
        except:
            self.mode_switch_error_dialog.open()
            return

        self.ids.status.text = "Mode set"
        # If we have been connected, reconnect
        if was_connected:
            self.start()


# Load the design file for this screen (.kv files)
# The path has to be relative to root of the app, i.e. where the biogascontrollerapp.py
# file is located
Builder.load_file("./gui/main/main.kv")
