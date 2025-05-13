"""
Library to be used in standalone mode (without microcontroller, for testing functionality)
It simulates the behviour of an actual microcontroller being connected
"""

from typing import Optional
import queue
import random
import serial
import time
import struct

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
    def __init__(
        self, baudrate: int = 19200, filters: Optional[list[str]] = None
    ) -> None:
        # Calling the constructor of the super class to assign defaults
        print("\n\nWARNING: Using testing library for communication!\n\n")
        super().__init__(baudrate, filters)

        # Initialize queue with values to be sent on call of recieve
        self.__simulated_data: queue.Queue[bytes] = queue.Queue()
        self.__simulated_data_remaining = 0

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
        data = []
        # If queue is too short, refill it
        if self.__simulated_data_remaining < byte_count:
            self.__fill_queue()

        for _ in range(byte_count):
            if self.__mode == "NM":
                time.sleep(0.001)
            try:
                data.append(self.__simulated_data.get_nowait())
                self.__simulated_data_remaining -= 1
            except Exception as e:
                print("ERROR: Simulation could not continue")
                raise SimulationError(
                    "Simulation encountered an error with the simulation queue. The error encountered: \n"
                    + str(e)
                )
        return b''.join(data)

    def send(self, msg: str) -> None:
        # Using LUT to reference
        readback = instruction_lut.get(msg)
        if readback != None:
            for i in range(len(readback)):
                self.__simulated_data.put(bytes(readback[i], "ascii"))
        if msg == "RD":
            # Handle ReadData readback
            # self.__simulated_data.put(ord(""))
            pass

    def send_float(self, msg: float) -> None:
        # Encode float as 8 bytes (64 bit)
        ba = struct.pack("d", msg)
        for byte in ba:
            self.__simulated_data.put(byte.to_bytes())

    def __fill_queue(self):
        # Add some dummy data. The data is randomized and is *not*
        # an accurate simulation of what the microcontroller will return
        # It only serves to check if the protocol handling works as expected
        for _ in range(4):
            self.__add_to_queue(self.__generate_int_as_bytes(200))
            self.__simulated_data.put(bytes(" ", "ascii"))
            self.__add_to_queue(self.__generate_float_as_bytes(size = 6))
            self.__simulated_data.put(bytes(" ", "ascii"))
            self.__simulated_data_remaining += 2
        for _ in range(3):
            self.__add_to_queue(self.__generate_int_as_bytes(65535))
            self.__simulated_data.put(bytes(" ", "ascii"))
        self.__add_to_queue(self.__generate_int_as_bytes(65535))
        self.__simulated_data.put(bytes("\n", "ascii"))
        self.__simulated_data_remaining += 4
        print("Length:", self.__simulated_data_remaining)

    def __generate_int_as_bytes(self, upper_limit: int) -> list[bytes]:
        byte_array = random.randint(0, upper_limit).to_bytes(4, "big")
        return [byte.to_bytes() for byte in byte_array]

    def __generate_float_as_bytes(self, upper_limit: int = 200, size: int = 4) -> list[bytes]:
        random_float = random.random() * upper_limit
        byte_data = struct.pack(">f", random_float)
        data = [byte.to_bytes() for byte in byte_data]
        for _ in range(size - len(data)):
            data.append(b'\x00')
        return data

    def __add_to_queue(self, data: list[bytes]):
        for value in data:
            self.__simulated_data_remaining += 1
            self.__simulated_data.put(value)
