from typing import Optional
import lib.com
import lib.decoder

# TODO: Load filters (for comport search)
com = lib.com.Com()
decoder = lib.decoder.Decoder()

class Instructions:
    def __init__(self) -> None:
        pass

    def _hook(self, instruction: str, sequence: list[str]) -> bool:
        return False

    def change_temperature(self, new_temps: list[float]) -> None:
        pass

    def change_config(self, new_config: list[float]) -> None:
        pass


