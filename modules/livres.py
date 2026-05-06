from sqlalchemy import Column, Integer, String
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from common.types.object_id_str import ObjectIdStr


class MetaModel(type(BaseModel)):
    def __getattr__(cls, item):
        if item.startswith('__pydantic_') or item in {'model_fields', '__fields__'}:
            raise AttributeError(f"{cls.__name__} has no attribute {item}")

        fields = getattr(cls, '__pydantic_fields__', {})

        if item in fields:
            return item

        for field_name, field_info in fields.items():
            field_type = getattr(field_info, 'outer_type_', None) or getattr(field_info, 'type_', None)

            if field_type and isinstance(field_type, type) and issubclass(field_type, BaseModel):
                nested_fields = getattr(field_type, '__fields__', {})
                if item in nested_fields:
                    return f"{field_name}.{item}"

        raise AttributeError(f"{cls.__name__} has no attribute {item}")


class LivreModel(BaseModel, metaclass=MetaModel):
    model_config = ConfigDict(populate_by_name=True)

    # id: ObjectIdStr = Field(alias="_id", default=None)

    titre: str
    auteur: str
    annee: Optional[int] = None
    isbn: Optional[str] = None


class LivrePatchModel(BaseModel, metaclass=MetaModel):
    titre: Optional[str] = None
    auteur: Optional[str] = None
    annee: Optional[int] = None
    isbn: Optional[str] = None


class LivreModelResult(BaseModel):
    total: int
    results: list[LivreModel]
