from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """Base model for Hume API responses."""

    def to_json_str(self) -> str:
        """Convert the model to a JSON string."""
        return self.model_dump_json(exclude_unset=True, by_alias=True)
