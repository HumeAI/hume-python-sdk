"""Hume API client exception."""


class HumeClientException(Exception):
    """Hume API client exception."""

    @classmethod
    def from_error(cls, error_code: str, error_message: str) -> "HumeClientException":
        return cls(f"hume({error_code}): {error_message}")
