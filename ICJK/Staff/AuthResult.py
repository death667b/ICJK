from enum import Enum

class AUTH_RESULT(Enum):
    NO_ERROR = 0
    SIGNUP_INVALID_EMAIL = 1
    SIGNUP_INVALID_PASSWORD = 2
    SIGNUP_INVALID_CONFIRMATION = 3
    SIGNUP_EMAIL_IN_USE = 4
    SIGNUP_OTHER = 5
    LOGIN_INVALID_COMBINATION = 6
    LOGIN_OTHER = 7
