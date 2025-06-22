from abc import ABC, abstractmethod
from typing import Optional
import serial

# If you don't know what OOP is, you can safely ignore this file
#
# The below class is abstract to have a consistent, targetable interface
# for both the real connection module and the simulation module
#
# For the interested, a quick rundown of what the benefits are of doing it this way is:
# This class provides a way to have two wholly different implementations that have
# the same function interface (i.e. all functions take the same arguments)
#
# Another benefit of having classes is that we can pass a single instance around to
# various components and have one shared instance that all can modify, reducing some
# overhead.
#
# The actual implementation of most functions (called methods in OOP) are implemented
# in the Com class below.


class ControllerConnection(ABC):
    def __init__(
        self, baudrate: Optional[int] = 19200, filters: Optional[list[str]] = None
    ) -> None:
        self._serial: Optional[serial.Serial] = None
        self._filters = (
            filters
            if filters != None
            else ["USB-Serial Controller", "Prolific USB-Serial Controller"]
        )
        self._port_override = ""
        self._baudrate = baudrate if baudrate != None else 19200
        self._err = None

    def set_port_override(self, override: str) -> None:
        """Set the port override, to disable port search"""
        if override != "" and override != "None":
            self._port_override = override

    def get_error(self) -> serial.SerialException | None:
        return self._err

    @abstractmethod
    def get_comport(self) -> str:
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def receive(self, byte_count: int) -> bytes:
        pass

    @abstractmethod
    def send(self, msg: str) -> None:
        pass

    @abstractmethod
    def send_float(self, msg: float) -> None:
        pass
