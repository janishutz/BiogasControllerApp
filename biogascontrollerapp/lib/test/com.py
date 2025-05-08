"""
Library to be used in standalone mode (without microcontroller, for testing functionality)
It simulates the behviour of an actual microcontroller being connected
"""

from typing import Optional
import queue
import random

# This file contains a Com class that can be used to test the functionality
# even without a microcontroller. It is not documented in a particularly
# beginner-friendly way, nor is the code written with beginner-friendliness
# in mind. It is the most complicated piece of code of the entire application

# All double __ prefixed properties are not available in the actual one


class Com:
    def __init__(self) -> None:
        # Initialize queue with values to be sent on call of recieve (add like three or so at a time)
        self._port_override = ""
        self.__mode = ""
        self.__simulated_data = queue.Queue()

    def set_port_override(self, override: str) -> None:
        """Set the port override, to disable port search"""
        self._port_override = override

    def get_comport(self) -> str:
        return "test" if self._port_override != "" else self._port_override

    def connect(self) -> bool:
        # TODO: For testing, make cases where there is no successful connection, i.e. we return false
        # Randomly return false
        if random.randint(0, 20):
            return False
        return True

    def close(self) -> None:
        pass

    def receive(self, byte_count: int) -> bytes:
        # TODO: Make it return simulated data
        return bytes("A", "ascii")

    def send(self, msg: str) -> None:
        # TODO: Use LUT to find what should be added to the queue for read
        # Using LUT to reference
        pass

    def send_float(self, msg: float) -> None:
        pass

    def _generate_random_value(self, precision: int) -> bytes:
        return bytes(str(round(random.random() * precision) / precision), "ascii")
