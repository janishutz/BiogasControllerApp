"""
Library to be used in standalone mode (without microcontroller, for testing functionality)
It simulates the behviour of an actual microcontroller being connected
"""

from typing import Optional
import queue
import random
import serial
import time

from lib.com import ComSuperClass

# This file contains a Com class that can be used to test the functionality
# even without a microcontroller. It is not documented in a particularly
# beginner-friendly way, nor is the code written with beginner-friendliness
# in mind. It is the most complicated piece of code of the entire application

# All double __ prefixed properties and methods are not available in the actual one

instruction_lut: dict[str, list[str]] = {
    "PR": ["\n", "P", "R", "\n"],
    "PT": ["\n", "P", "T", "\n"],
    "RD": ["\n", "R", "D", "\n"],
    "NM": ["\n", "N", "M", "\n"],
    "FM": ["\n", "F", "M", "\n"],
}


class SimulationError(Exception):
    pass


class Com(ComSuperClass):
    def __init__(self, baudrate: int = 19200, filters: Optional[list[str]] = None) -> None:
        # Calling the constructor of the super class to assign defaults
        print("\n\nWARNING: Using testing library for communication!\n\n")
        super().__init__(baudrate, filters);

        # Initialize queue with values to be sent on call of recieve
        self.__simulated_data: queue.Queue[int] = queue.Queue()
        self.__simulated_data_remaining = 0

        # Keep track of the number of bytes sent to fulfil protocol
        self.__bytes_sent: int = 0

        # Initially, we are in normal mode (which leads to slower data intervals)
        self.__mode = "NM"

    def set_port_override(self, override: str) -> None:
        """Set the port override, to disable port search"""
        self._port_override = override

    def get_error(self) -> serial.SerialException | None:
        pass

    def get_comport(self) -> str:
        return "test" if self._port_override != "" else self._port_override

    def connect(self) -> bool:
        # Randomly return false in 1 in 20 ish cases
        if random.randint(0, 20) == 1:
            print("Simulating error to connect")
            return False
        return True

    def close(self) -> None:
        pass

    def receive(self, byte_count: int) -> bytes:
        # TODO: Make it return simulated data -> Refill if queue length is smaller than requested byte_count
        data = []
        # If queue is too short, refill it
        if self.__simulated_data_remaining < byte_count:
            self.__fill_queue()

        for i in range(byte_count):
            if self.__mode == "NM":
                time.sleep( 0.001 );
            try:
                data.append(self.__simulated_data.get_nowait())
            except Exception as e:
                print("ERROR: Simulation could not continue")
                raise SimulationError("Simulation encountered an error with the simulation queue. The error encountered: \n" + str(e))
        return bytes(data)

    def send(self, msg: str) -> None:
        # TODO: Use LUT to find what should be added to the queue for read
        # Using LUT to reference
        readback = instruction_lut.get(msg)
        if readback != None:
            for i in range(len(readback)):
                self.__simulated_data.put(ord(readback[i]))

    def send_float(self, msg: float) -> None:
        pass

    def __add_random_float(self):
        pass

    def __fill_queue(self):
        pass
