"""
Library to be used in standalone mode (without microcontroller, for testing functionality)
"""

from typing import Optional
import queue


class Com:
    def __init__(self) -> None:
        # Initialize queue with values to be sent on call of recieve (add like three or so at a time)
        self._port_override = ''

    def set_port_override(self, override: str) -> None:
        """Set the port override, to disable port search"""
        self._port_override = override

    def get_comport(self) -> str:
        return 'test' if self._port_override != '' else self._port_override

    def connect(self, baud_rate: int, port_override: Optional[str] = None) -> bool:
        return True # TODO: For testing, make cases where there is no successful connection, i.e. we return false

    def close(self) -> None:
        pass

    def receive(self, byte_count: int) -> None:
        # TODO: Make it return simulated data
        pass

    def send(self, msg: str) -> None:
        # TODO: Use LUT to find what should be added to the queue for read
        pass

    def send_float(self, msg: float) -> None:
        pass
