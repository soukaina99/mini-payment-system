import enum


class AccountStatus(enum.Enum):
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'
    PAUSED = 'PAUSED'


class TransactionStatus(enum.Enum):
    INIT = 'INIT'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class TransactionType(enum.Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
