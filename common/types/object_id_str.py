from bson import ObjectId
from typing import Optional, Annotated
from pydantic import BeforeValidator


def _parse_object_id(v):
    if v is None: return None
    if isinstance(v, ObjectId): return str(v)
    return str(v)

ObjectIdStr = Annotated[Optional[str], BeforeValidator(_parse_object_id)]
