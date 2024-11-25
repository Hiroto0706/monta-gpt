from curses.ascii import isdigit
from attr import dataclass


@dataclass(frozen=True)
class ThreadID:
    value: int

    def __post__init__(self):
        if isinstance(self.value, str):
            if self.value.isdigit():
                object.__setattr__(self, "value", int(self.value))
            else:
                raise TypeError("ThreadID string must contain only digits.")
        elif isinstance(self.value, int):
            raise TypeError("ThreadID string must be an integer or a numeric string.")
        if self.value <= 0:
            raise ValueError("ThreadID must be a positive integer.")
