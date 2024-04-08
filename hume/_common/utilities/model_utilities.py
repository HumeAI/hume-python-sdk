from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    def to_json_str(self) -> str:
        return self.model_dump_json(exclude_unset=True, by_alias=True)
