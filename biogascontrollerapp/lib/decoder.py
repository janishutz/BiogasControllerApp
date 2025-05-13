import struct

class Decoder:
    def decode_ascii(self, value: bytes) -> str:
        try:
            return value.decode()
        except:
            return 'Error'

    def decode_float(self, value: bytes) -> float:
        return struct.unpack('>f', bytes.fromhex(str(value, 'ascii') + '00'))[0]

    def decode_float_long(self, value: bytes) -> float:
        return struct.unpack('>f', bytes.fromhex(str(value, 'ascii') + '0000'))[0]

    def decode_int(self, value: bytes) -> int:
        # return int.from_bytes(value, 'big')
        return int(value, base=16)
