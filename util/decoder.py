import struct


# Decoder to decode various sent values from the microcontroller
class Decoder:
    # Decode an ascii character
    def decode_ascii(self, value: bytes) -> str:
        try:
            return value.decode()
        except:
            return "Error"

    # Decode a float (6 bits)
    def decode_float(self, value: bytes) -> float:
        return struct.unpack(">f", bytes.fromhex(str(value, "ascii") + "00"))[0]

    # Decode a float, but with additional offsets
    def decode_float_long(self, value: bytes) -> float:
        return struct.unpack(">f", bytes.fromhex(str(value, "ascii") + "0000"))[0]

    # Decode an int
    def decode_int(self, value: bytes) -> int:
        # return int.from_bytes(value, 'big')
        return int(value, base=16)
