from abc import ABC, abstractmethod
from typing import Optional
import serial
import struct
import serial.tools.list_ports


class ComSuperClass(ABC):
    def __init__(self, baudrate: int = 19200, filters: Optional[list[str]] = None) -> None:
        self._serial: Optional[serial.Serial] = None
        self._filters = filters if filters != None else [ 'USB-Serial Controller', 'Prolific USB-Serial Controller' ]
        self._port_override = ''
        self._baudrate = baudrate
        self._err = None

    def set_port_override(self, override: str) -> None:
        """Set the port override, to disable port search"""
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


class Com(ComSuperClass):
    def _connection_check(self) -> bool:
        if self._serial == None:
            return self._open()
        if self._serial != None:
            if not self._serial.is_open:
                self._serial.open()
            return True
        else:
            return False

    def get_comport(self) -> str:
        """Find the comport the microcontroller has attached to"""
        if self._port_override != '':
            return self._port_override

        # Catch all errors and simply return an empty string if search unsuccessful
        try:
            # Get an array of all used comports
            ports = [comport.device for comport in serial.tools.list_ports.comports()]

            # Filter for specific controller
            for comport in ports:
                for filter in self._filters:
                    if ( filter in comport ):
                        return comport
        except Exception as e:
            self._err = e

        return ""

    def _open(self) -> bool:
        comport = self.get_comport()

        # Comport search returns empty string if search unsuccessful
        if comport == '':
            try:
                self._serial = serial.Serial(comport, self._baudrate, timeout=5)
            except serial.SerialException as e:
                self._err = e
                return False
            return True
        else:
            return False

    def connect(self) -> bool:
        """Try to find a comport and connect to the microcontroller. Returns the success as a boolean"""
        return self._connection_check()

    def close(self) -> None:
        """Close the serial connection, if possible"""
        if self._serial != None:
            try:
                self._serial.close()
            except:
                pass

    def receive(self, byte_count: int) -> bytes:
        """Recieve bytes from microcontroller over serial. Returns bytes. Might want to decode using functions from lib.tools"""
        self._connection_check()
        if self._serial != None:
            return self._serial.read(byte_count)
        else:
            raise Exception('ERR_CONNECTING')

    def send(self, msg: str) -> None:
        """Send a string over serial connection. Will open a connection if none is available"""
        self._connection_check()
        if self._serial != None:
            self._serial.write(msg.encode())
        else:
            raise Exception('ERR_CONNECTING')

    def send_float(self, msg: float) -> None:
        """Send a float number over serial connection"""
        self._connection_check()
        if self._serial != None:
            self._serial.write(bytearray(struct.pack('>f', msg))[0:3])
        else:
            raise Exception('ERR_CONNECTING')
