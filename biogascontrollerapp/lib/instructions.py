from lib.com import Com
import lib.decoder
import time

# TODO: Load filters (for comport search)
decoder = lib.decoder.Decoder()


# Class that supports sending instructions to the microcontroller,
# as well as hooking to data stream according to protocol
class Instructions:
    def __init__(self, com: Com) -> None:
        self._com = com

    # Set a port override (to use a specific COM port)
    def set_port_override(self, override: str) -> None:
        self._com.set_port_override(override)

    # Helper method to hook to the data stream according to protocol.
    # You can specify the sequence that the program listens to to sync up,
    # as an array of strings, that should each be of length one and only contain
    # ascii characters
    def hook(self, instruction: str, sequence: list[str]) -> bool:
        # Add protection: If we cannot establish connection, refuse to run
        if not self._com.connect():
            return False

        # Send instruction to microcontroller to start hooking process
        # If instruction is an empty string, do not send instruction

        if instruction != "":
            self._com.send(instruction)

        # Record start time to respond to timeout
        start = time.time()

        # The pointer below points to the element in the array which is the next expected character to be received
        pointer = 0

        # Simply the length of the sequence, since it is both cheaper and cleaner to calculate it once
        sequence_max = len(sequence)

        # Only run for a limited amount of time
        while time.time() - start < 5:
            # If the decoded ascii character is equal to the next expected character, move pointer right by one
            # If not, jump back to start
            if (decoder.decode_ascii(self._com.receive(1))) == sequence[pointer]:
                pointer += 1
            else:
                pointer = 0

            # If the pointer has reached the end of the sequence, return True, as now the hook was successful
            if pointer == sequence_max:
                return True

        # If we time out, which is the only way in which this code can be reached, return False
        return False

    # Private helper method to transmit data using the necessary protocols
    def _change_data(
        self,
        instruction: str,
        readback: list[str],
        data: list[float],
        readback_length: int,
    ) -> None:
        # Hook to stream
        if self.hook(instruction, readback):
            # Transmit data
            while len(data) > 0:
                # If we received data back, we can send more data, i.e. from this we know
                # the controller has received the data
                # If not, we close the connection and create an exception
                if self._com.receive(readback_length) != "":
                    self._com.send_float(data.pop(0))
                else:
                    self._com.close()
                    raise Exception(
                        "Failed to transmit data. No response from controller"
                    )
            self._com.close()
        else:
            self._com.close()
            raise ConnectionError(
                "Failed to hook to controller data stream. No fitting response received"
            )

    # Abstraction of the _change_data method specifically designed to change the entire config
    def change_config(self, new_config: list[float]) -> None:
        try:
            self._change_data("PR", ["\n", "P", "R", "\n"], new_config, 3)
        except Exception as e:
            raise e

    # Abstraction of the _change_data method specifically designed to change only the configured temperature
    def change_temperature(self, temperatures: list[float]) -> None:
        try:
            self._change_data("PT", ["\n", "P", "T", "\n"], temperatures, 3)
        except Exception as e:
            raise e
