import util.decoder
import time

from util.interface import ControllerConnection

decoder = util.decoder.Decoder()


# Class that supports sending instructions to the microcontroller,
# as well as hooking to data stream according to protocol
class Instructions:
    def __init__(self, com: ControllerConnection) -> None:
        self._com = com

    # Helper method to hook to the data stream according to protocol.
    # You can specify the sequence that the program listens to to sync up,
    # as an array of strings, that should each be of length one and only contain
    # ascii characters
    def hook(self, instruction: str, sequence: list[str]) -> bool:
        # Add protection: If we cannot establish connection, refuse to run
        if not self._com.connect():
            return False

        # Send instruction to microcontroller to start hooking process
        self._com.send(instruction)

        # Record start time to respond to timeout
        start = time.time()

        # The pointer below points to the element in the array which is the next expected character to be received
        pointer = 0

        # Simply the length of the sequence, since it is both cheaper and cleaner to calculate it once
        sequence_max = len(sequence)

        # Only run for a limited amount of time
        while time.time() - start < 5:
            # Receive and decode a single byte and decode as ASCII
            data = decoder.decode_ascii(self._com.receive(1))
            if data == sequence[pointer]:
                # Increment the pointer (move to next element in the List)
                pointer += 1
            else:
                # Jump back to start
                pointer = 0

            # If the pointer has reached the end of the sequence, return True, as now the hook was successful
            if pointer == sequence_max:
                return True

        # If we time out, which is the only way in which this code can be reached, return False
        return False

    # Used to hook to the main data stream, as that hooking mechanism is different
    def hook_main(self) -> bool:
        # Record start time to respond to timeout
        start = time.time()

        # Wait to find a CR character (enter)
        char = decoder.decode_ascii(self._com.receive(1))
        while char != "\n":
            # Check for timeout
            if time.time() - start > 3:
                return False

            # Set the next character by receiving and decoding it as ASCII
            char = decoder.decode_ascii(self._com.receive(1))

        # Store the position in the hooking process
        state = 0
        distance = 0

        # While we haven't timed out and have not reached the last state execute
        # The last state indicates that the sync was successful
        while time.time() - start < 5 and state < 3:
            # Receive the next char and decode it as ASCII
            char = decoder.decode_ascii(self._com.receive(1))

            # The character we look for when syncing is Space (ASCII char 32 (decimal))
            # It is sent every 4 bits. If we have received 3 with the correct distance from
            # the previous in a row, we are synced
            if char == " ":
                if distance == 4:
                    state += 1
                distance = 0
            else:
                if distance > 4:
                    state = 0
                    distance = 0
                else:
                    distance += 1

        # Read 5 more bits to correctly sync up
        self._com.receive(5)

        return state == 3

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
