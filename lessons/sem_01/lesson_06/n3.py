import io
import sys
from enum import Enum
from typing import Union

class FileOutModes(Enum):
    APPEND = "a"
    REWRITE = "w"

class FileOut:
    def __init__(self, path_to_file: str, mode: Union[str, FileOutModes] = FileOutModes.REWRITE) -> None:
        if isinstance(mode, str):
            if mode not in [FileOutModes.REWRITE.value, FileOutModes.APPEND.value]:
                raise ValueError("Mode should be 'w' or 'a'")
            self.mode = FileOutModes(mode)
        elif isinstance(mode, FileOutModes):
            self.mode = mode
        else:
            raise ValueError("Mode should be 'w' or 'a'")

        self.path_to_file = path_to_file
        self._original_stdout = sys.stdout
        self._file = None

    def __enter__(self) -> 'FileOut':
        self._file = open(self.path_to_file, self.mode.value)
        sys.stdout = self._file
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        sys.stdout = self._original_stdout
        if self._file:
            self._file.close()