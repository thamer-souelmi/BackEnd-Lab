from pydantic import BaseModel, Field
from typing import Optional
from pymongoose.mongo_types import Schema,Types
from modules.livres import LivreModel
from pymongoose import methods


class LivreSchema(Schema):
    schema_name = "Livre"

    def __init__(self, **kwargs):
        self.schema = {
            LivreModel.id: {
                "type": Types.ObjectId,
                "required": True
            },
            LivreModel.titre: {
                "type": Types.String,
                "required": True
            },
            LivreModel.auteur: {
                "type": Types.String,
                "required": True
            },
            LivreModel.annee: {
                "type": Types.Number,
                "required": False
            },
            LivreModel.isbn: {
                "type": Types.String,
                "required": False
            }

        }
        super().__init__(self.schema_name, self.schema, kwargs)
        self.native_collection = methods.database.get_collection(
            self.schema_name,
        )


class LivreCreation(BaseModel):
    titre: str = Field(..., min_length=1)
    auteur: str = Field(..., min_length=1)
    annee: Optional[int] = None
    isbn: Optional[str] = None


class LivreMiseAJour(BaseModel):
    titre: Optional[str]
    auteur: Optional[str]
    annee: Optional[int]
    isbn: Optional[str]


livre_schema = LivreSchema
methods.schemas["Livre"] = livre_schema


class LivreReponse(LivreCreation):
    id: int

    class Config:
        from_attributes = True