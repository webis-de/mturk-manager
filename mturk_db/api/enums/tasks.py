from enum import IntEnum, unique

@unique
class STATUS_TASK(IntEnum):
    CREATED = 0
    PROGRESS = 1
    FINISHED = 2
    FAILED = 3
