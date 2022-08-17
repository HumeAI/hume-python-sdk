from enum import Enum


class BatchJobStatus(Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    QUEUED = "QUEUED"

    @classmethod
    def is_terminal(cls, status: "BatchJobStatus") -> bool:
        return status in [cls.COMPLETED, cls.FAILED]

    @classmethod
    def from_str(cls, status: str) -> "BatchJobStatus":
        for _, enum_value in cls.__members__.items():
            if enum_value.value == status:
                return enum_value
        raise ValueError(f"Unknown status '{status}'")
