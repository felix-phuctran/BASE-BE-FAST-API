from enum import Enum


class BaseEnum(Enum):

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, Enum):
            return self.value == other.value
        return False

