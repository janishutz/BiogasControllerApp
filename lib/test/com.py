"""
Library to be used in standalone mode (without microcontroller, for testing functionality)
It simulates the behviour of an actual microcontroller being connected
"""

from typing import List, Optional
import queue
import random
import time
import struct

from lib.com import ComSuperClass

# ┌                                                ┐
# │             Testing Module For Com             │
# └                                                ┘
# This file contains a Com class that can be used to test the functionality
# even without a microcontroller. It is not documented in a particularly
# beginner-friendly way, nor is the code written with beginner-friendliness
# in mind. It is the most complicated piece of code of the entire application

# ────────────────────────────────────────────────────────────────────

# All double __ prefixed properties and methods are not available in the actual impl

instruction_lut: dict[str, list[str]] = {
    "PR": ["\n", "P", "R", "\n"],
    "PT": ["\n", "P", "T", "\n"],
    "RD": ["\n", "R", "D", "\n"],
    "NM": ["\n", "N", "M", "\n"],
    "FM": ["\n", "F", "M", "\n"],
}

reconfig = ["a", "b", "c", "t"]


class SimulationError(Exception):
    pass


class SensorConfig:
    a: float
    b: float
    c: float
    t: float

    def __init__(
        self, a: float = 20, b: float = 30, c: float = 10, t: float = 55
    ) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.t = t


class Com(ComSuperClass):
    def __init__(
        self, fail_sim: int, baudrate: int = 19200, filters: Optional[list[str]] = None
    ) -> None:
        # Calling the constructor of the super class to assign defaults
        print("\n\nWARNING: Using testing library for communication!\n\n")
        super().__init__(baudrate, filters)

        # Initialize queue with values to be sent on call of recieve
        self.__simulated_data: queue.Queue[bytes] = queue.Queue()
        self.__simulated_data_remaining = 0

        self.__reconf_sensor = 0
        self.__reconf_step = 0
        self.__fail_sim = fail_sim

        self.__config: List[SensorConfig] = [
            SensorConfig(),
            SensorConfig(),
            SensorConfig(),
            SensorConfig(),
        ]

        # Initially, we are in normal mode (which leads to slower data intervals)
        self.__mode = "NM"

    def set_port_override(self, override: str) -> None:
        """Set the port override, to disable port search"""
        self._port_override = override

    def get_comport(self) -> str:
        return "Sim" if self._port_override == "" else self._port_override

    def connect(self) -> bool:
        # Randomly return false in 1 in fail_sim ish cases
        if random.randint(0, self.__fail_sim) == 0:
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
                time.sleep(0.005)
            try:
                data.append(self.__simulated_data.get_nowait())
                self.__simulated_data_remaining -= 1
            except Exception as e:
                print("ERROR: Simulation could not continue")
                raise SimulationError(
                    "Simulation encountered an error with the simulation queue. The error encountered: \n"
                    + str(e)
                )
        return b"".join(data)

    def send(self, msg: str) -> None:
        # Using LUT to reference
        readback = instruction_lut.get(msg)
        if readback != None:
            for i in range(len(readback)):
                self.__add_ascii_char(readback[i])
        if msg == "RD":
            self.__set_read_data_data()
        elif msg == "PR":
            self.__reconf_sensor = 0
            self.__reconf_step = 0
            self.__add_ascii_char("a")
            self.__add_ascii_char("0")
            self.__add_ascii_char("\n")

    def __set_read_data_data(self) -> None:
        # Send data for all four sensors
        for i in range(4):
            self.__add_float_as_hex(self.__config[i].a)
            self.__add_ascii_char(" ")
            self.__add_float_as_hex(self.__config[i].b)
            self.__add_ascii_char(" ")
            self.__add_float_as_hex(self.__config[i].c)
            self.__add_ascii_char(" ")
            self.__add_float_as_hex(self.__config[i].t)
            self.__add_ascii_char("\n")

    def send_float(self, msg: float) -> None:
        if self.__reconf_step == 0:
            self.__config[self.__reconf_sensor].a = msg
        elif self.__reconf_step == 1:
            self.__config[self.__reconf_sensor].b = msg
        elif self.__reconf_step == 2:
            self.__config[self.__reconf_sensor].c = msg
        elif self.__reconf_step == 3:
            self.__config[self.__reconf_sensor].t = msg

        if self.__reconf_step == 3:
            self.__reconf_step = 0
            self.__reconf_sensor += 1
        else:
            self.__reconf_step += 1

        if self.__reconf_sensor == 4:
            return

        self.__add_ascii_char(reconfig[self.__reconf_step])
        self.__add_ascii_char(str(self.__reconf_sensor))
        self.__add_ascii_char("\n")

    def __fill_queue(self):
        # Simulate a full cycle
        for _ in range(4):
            self.__add_integer_as_hex(self.__generate_random_int(200))
            self.__simulated_data.put(bytes(" ", "ascii"))
            self.__add_float_as_hex(self.__generate_random_float(50))
            self.__simulated_data.put(bytes(" ", "ascii"))
            self.__simulated_data_remaining += 2
        for _ in range(3):
            self.__add_integer_as_hex(self.__generate_random_int(65535))
            self.__simulated_data.put(bytes(" ", "ascii"))
            self.__simulated_data_remaining += 1
        self.__add_integer_as_hex(self.__generate_random_int(65535))
        self.__simulated_data.put(bytes("\n", "ascii"))
        self.__simulated_data_remaining += 1

    def __generate_random_int(self, max: int) -> int:
        return random.randint(0, max)

    def __generate_random_float(self, max: int) -> float:
        return random.random() * max

    def __add_ascii_char(self, ascii_string: str):
        self.__simulated_data.put(ord(ascii_string).to_bytes(1))
        self.__simulated_data_remaining += 1

    def __add_two_byte_value(self, c: int):
        """putchhex

        Args:
            c: The char (as integer)
        """
        # First nibble (high)
        high_nibble = (c >> 4) & 0x0F
        high_char = chr(high_nibble + 48 if high_nibble < 10 else high_nibble + 55)
        self.__simulated_data.put(high_char.encode())

        # Second nibble (low)
        low_nibble = c & 0x0F
        low_char = chr(low_nibble + 48 if low_nibble < 10 else low_nibble + 55)
        self.__simulated_data.put(low_char.encode())
        self.__simulated_data_remaining += 2

    def __add_integer_as_hex(self, c: int):
        """Writes the hexadecimal representation of the high and low bytes of integer `c` (16-bit) to the simulated serial port."""
        if not (0 <= c <= 0xFFFF):
            raise ValueError("Input must be a 16-bit integer (0–65535)")

        # Get high byte (most significant byte)
        hi_byte = (c >> 8) & 0xFF
        # Get low byte (least significant byte)
        lo_byte = c & 0xFF

        # Call putchhex for the high byte and low byte
        self.__add_two_byte_value(hi_byte)
        self.__add_two_byte_value(lo_byte)

    def __add_float_as_hex(self, f: float):
        """Converts a float to its byte representation and sends the bytes using putchhex."""
        # Pack the float into bytes (IEEE 754 format)
        packed = struct.pack(">f", f)  # Big-endian format (network byte order)

        # Unpack the bytes into 3 bytes: high, mid, low
        high, mid, low = packed[0], packed[1], packed[2]

        # Send each byte as hex
        self.__add_two_byte_value(high)
        self.__add_two_byte_value(mid)
        self.__add_two_byte_value(low)
