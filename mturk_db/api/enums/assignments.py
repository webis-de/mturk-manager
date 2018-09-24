from enum import IntEnum, unique

@unique
class STATUS_EXTERNAL(IntEnum):
    APPROVED = 0
    REJECTED = 1
    SUBMITTED = 2
    APPROVED_OVERRIDE = 3

@unique
class STATUS_INTERNAL(IntEnum):
    APPROVED = 0
    REJECTED = 1