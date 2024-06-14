"""Hume API client exception."""

from __future__ import annotations


class HumeClientException(Exception):
    """Hume API client exception."""

    @classmethod
    def from_error(cls, error_code: str, error_message: str) -> "HumeClientException":
        """Create an exception from an error.

        Args:
            error_code (str): Error code associated with the given error.
            error_message (str): Error message.

        Returns:
            HumeClientException: Exception object with the formatted error message.
        """
        return cls(f"hume({error_code}): {error_message}")
