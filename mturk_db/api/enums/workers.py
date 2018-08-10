from enum import IntEnum, unique

@unique
class STATUS_BLOCK(IntEnum):
    NONE = 1
    SOFT = 2
    HARD = 3