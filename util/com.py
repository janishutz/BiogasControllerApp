from typing import override
import serial
import struct
import serial.tools.list_ports

from util.interface import ControllerConnection


# ┌                                                ┐
# │         Main Com Class Implementation          │
# └                                                ┘
# Below you can find what you were most likely looking for. This is the implementation of the communication with the microcontroller.
# You may also be interested in the decoder.py and instructions.py file, as the decoding and the hooking / syncing process are
# implemented there. It is recommended that you do NOT read the test/com.py file, as that one is only there for simulation purposes
# and is much more complicated than this here, if you are not well versed with Python or are struggling with the basics

# All variables starting in self are bound to the object and can be changed by any consumer of this library. The Com class
# inherits from the ControllerConnection class (found in interface.py), which implements some of the methods (functions)
# this class exposes, namely the constructor, set_port_override and get_error. They are not further relevant for the code below
# though, so you can safely ignore it.


class Com(ControllerConnection):
    def _connection_check(self) -> bool:
        if self._serial == None:
            return self._open()
        if self._serial != None:
            if not self._serial.is_open:
                self._serial.open()
            return True
        else:
            return False

    @override
    def get_comport(self) -> str:
        """Find the comport the microcontroller has attached to"""
        if self._port_override != "":
            return self._port_override

        # Catch all errors and simply return an empty string if search unsuccessful
        try:
            # Get an array of all used comports
            ports = [comport.device for comport in serial.tools.list_ports.comports()]

            # Filter for specific controller
            for comport in ports:
                for filter in self._filters:
                    if filter in comport:
                        return comport
        except Exception as e:
            self._err = e

        return ""

    def _open(self) -> bool:
        """Open the connection. Internal function, not to be called directly, use connect instead

        Returns:
            Boolean indicates if connection was successful or not
        """
        # Get the com port the controller has connected to
        comport = self.get_comport()

        # Comport search returns empty string if search unsuccessful
        if comport != "":
            # Try to generate a new Serial object with the configuration of this class
            # self._baudrate contains the baud rate and defaults to 19200
            try:
                self._serial = serial.Serial(comport, self._baudrate, timeout=5)
            except serial.SerialException as e:
                # If an error occurs, catch it, handle it and store the error
                # for the UI and return False to indicate failed connection
                self._err = e
                return False

            # Connection succeeded, return True
            return True
        else:
            # Haven't found a comport
            return False

    @override
    def connect(self) -> bool:
        """Try to find a comport and connect to the microcontroller. Returns the success as a boolean"""
        return self._connection_check()

    @override
    def close(self) -> None:
        """Close the serial connection, if possible"""
        if self._serial != None:
            try:
                self._serial.close()
            except:
                pass

    @override
    def receive(self, byte_count: int) -> bytes:
        """Receive bytes from microcontroller over serial. Returns bytes. Might want to decode using functions from lib.decoder"""
        # Check connection
        self._connection_check()

        # Ignore this boilerplate (extra code), the body of the if is the only thing important.
        # The reason for the boilerplate is that the type checker will notice that self._serial can be
        # None, thus showing errors.
        if self._serial != None:
            return self._serial.read(byte_count)
        else:
            raise Exception("ERR_CONNECTING")

    @override
    def send(self, msg: str) -> None:
        """Send a string over serial connection. Will open a connection if none is available"""
        # Check connection
        self._connection_check()

        # Ignore this boilerplate (extra code), the body of the if is the only thing important.
        # The reason for the boilerplate is that the type checker will notice that self._serial can be
        # None, thus showing errors.
        if self._serial != None:
            self._serial.write(msg.encode())
        else:
            raise Exception("ERR_CONNECTING")

    @override
    def send_float(self, msg: float) -> None:
        """Send a float number over serial connection"""
        # Check connection
        self._connection_check()

        # Ignore this boilerplate (extra code), the body of the if is the only thing important.
        # The reason for the boilerplate is that the type checker will notice that self._serial can be
        # None, thus showing errors.
        if self._serial != None:
            self._serial.write(bytearray(struct.pack(">f", msg))[0:3])
        else:
            raise Exception("ERR_CONNECTING")
