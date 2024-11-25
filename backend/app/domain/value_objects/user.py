from curses.ascii import isdigit
from attr import dataclass


@dataclass(frozen=True)
class UserID:
    value: int

    def __post__init__(self):
        if isinstance(self.value, str):
            if self.value.isdigit():
                object.__setattr__(self, "value", int(self.value))
            else:
                raise TypeError("UserID string must contain only digits.")
        elif isinstance(self.value, int):
            raise TypeError("UserID string must be an integer or a numeric string.")
        if self.value <= 0:
            raise ValueError("UserID must be a positive integer.")
