"""Batch job status."""
from enum import Enum


class BatchJobStatus(Enum):
    """Batch job status."""

    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    QUEUED = "QUEUED"

    @classmethod
    def is_terminal(cls, status: "BatchJobStatus") -> bool:
        """Check if a status is "terminal".

        Args:
            status (BatchJobStatus): Status to check.

        Returns:
            bool: Whether the status is "terminal".
        """
        return status in [cls.COMPLETED, cls.FAILED]

    @classmethod
    def from_str(cls, status: str) -> "BatchJobStatus":
        """Convert a status to a string.

        Args:
            status (str): Status to convert.

        Returns:
            BatchJobStatus: The enum variant for the given string.
        """
        for _, enum_value in cls.__members__.items():
            if enum_value.value == status:
                return enum_value
        raise ValueError(f"Unknown status '{status}'")
