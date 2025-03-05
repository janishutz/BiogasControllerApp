import lib.com
import lib.decoder
import time

# TODO: Load filters (for comport search)
com = lib.com.Com()
decoder = lib.decoder.Decoder()

class Instructions:
    def set_port_override(self, override: str) -> None:
        com.set_port_override(override)

    def _hook(self, instruction: str, sequence: list[str]) -> bool:
        # Send instruction to microcontroller to start hooking process
        com.send(instruction)
        
        # Record start time to respond to timeout
        start = time.time()

        # Check for timeout
        pointer = 0
        sequence_max = len(sequence) - 1
        while time.time() - start < 5:
            if ( decoder.decode_ascii( com.receive(1) ) ) == sequence[pointer]:
                pointer += 1
            else:
                pointer = 0

            if pointer == sequence_max:
                return True

        return False

    def _change_data(self, instruction: str, readback: list[str], data: list[float], readback_length: int) -> None:
        # Hook to stream
        if self._hook(instruction, readback):
            while len(data) > 0:
                if com.receive(readback_length) != '':
                    com.send_float(data.pop(0))
                else:
                    com.close()
                    raise Exception('Failed to transmit data. No response from controller')
            com.close()
        else:
            com.close()
            raise ConnectionError('Failed to hook to controller data stream. No fitting response received')

    def change_config(self, new_config: list[float]) -> None:
        self._change_data('PR', ['\n', 'P', 'R', '\n'], new_config, 3)

    def change_temperature(self, temperatures: list[float]) -> None:
        self._change_data('PT', ['\n', 'P', 'T', '\n'], temperatures, 3)

    def enable_fastmode(self) -> None:
        com.send('FM')
        com.close()

    def disable_fastmode(self) -> None:
        com.send('NM')
        com.close()

