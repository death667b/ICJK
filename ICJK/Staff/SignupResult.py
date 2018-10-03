from enum import Enum

class SIGNUP_RESULT(Enum):
    NO_ERROR = 0
    INVALID_EMAIL = 1
    INVALID_PASSWORD = 2
    INVALID_CONFIRMATION = 3
    EMAIL_IN_USE = 4
    OTHER = 5
