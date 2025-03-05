from typing import Optional
import serial
import struct
import serial.tools.list_ports


class Com:
    def __init__(self, filters: Optional[list[str]] = None) -> None:
        self._serial: Optional[serial.Serial] = None
        self._filters = filters if filters != None else [ 'USB-Serial Controller', 'Prolific USB-Serial Controller' ]
        self._port_override = ''

    def set_port_override(self, override: str) -> None:
        """Set the port override, to disable port search"""
        self._port_override = override

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
        except:
            pass

        return ''

    def connect(self, baud_rate: int, port_override: Optional[str] = None) -> bool:
        """Try to find a comport and connect to the microcontroller. Returns the success as a boolean"""
        comport = self.get_comport()

        # Comport search returns empty string if search unsuccessful
        if comport == '':
            try:
                self._serial = serial.Serial(comport, baud_rate, timeout=5)
            except:
                return False
            return True
        else:
            return False

    def close(self) -> None:
        """Close the serial connection, if possible"""
        if self._serial != None:
            try:
                self._serial.close()
            except:
                pass

    def receive(self, byte_count: int) -> bytes:
        """Recieve bytes from microcontroller over serial. Returns bytes. Might want to decode using functions from lib.tools"""
        if self._serial == None:
            self.connect(19200)
        if self._serial != None:
            return self._serial.read(byte_count)
        else:
            raise Exception('ERR_CONNECTION')

    def send(self, msg: str) -> None:
        """Send a string over serial connection."""
        if self._serial == None:
            self.connect(19200)
        if self._serial != None:
            self._serial.write(msg.encode())

    def send_float(self, msg: float) -> None:
        """Send a float number over serial connection"""
        if self._serial == None:
            self.connect(19200)
        if self._serial != None:
            self._serial.write(bytearray(struct.pack('>f', msg))[0:3])
