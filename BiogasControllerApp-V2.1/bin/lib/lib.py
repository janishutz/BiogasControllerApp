import serial
import struct
import bin.lib.comport_search
"""@package docstring
This package can communicate with a microcontroller"""

coms = bin.lib.comport_search.ComportService()


class Com:
    def __init__(self):
        self.xr = ""
        self.output = ""
        self.str_input = ""
        self.str_get_input = ""
        self.xs = ""
        self.__comport = '/dev/ttyUSB0'

    def connect(self, baudrate, special_port):
        try:
            self.__comport = coms.get_comport(special_port)
        except:
            pass
        self.ser = serial.Serial(self.__comport, baudrate=baudrate, timeout=5)

    def quitcom(self):
        try:
            self.ser.close()
        except:
            pass

    def receive(self, amount_bytes):
        self.xr = self.ser.read(amount_bytes)
        return self.xr

    def decode_ascii(self, value):
        try:
            self.output = value.decode()
        except:
            self.output = "Error"
        return self.output

    def check_value(self, value_check, checked_value):
        if value_check == checked_value:
            return 1
        else:
            return 0

    def decode_int(self, value):
        self.i = int(value, base = 16)
        return self.i

    def decode_float(self, value):
        self.fs = str(value, 'ascii') + '00'
        self.f = struct.unpack('>f', bytes.fromhex(self.fs))
        return str(self.f[0])

    def decode_float_2(self, value):
        self.fs = str(value, 'ascii') + '0000'
        self.f = struct.unpack('>f', bytes.fromhex(self.fs))
        return str(self.f[0])

    def get_input(self):
        self.str_get_input = input("please enter a character to send: ")
        return self.str_get_input

    def send(self, str_input):
        self.xs = str_input.encode()
        self.ser.write(self.xs)

    def send_float(self, float_input):
        ba = bytearray(struct.pack('>f', float_input))
        self.ser.write(ba[0:3])
