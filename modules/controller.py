from fastapi import APIRouter, HTTPException
from http import HTTPStatus

from modules.service import BookService
from modules.livres import LivreModel
from common.helpers.filters import Filters
from auth.deps import verify_token
from fastapi import Depends

router = APIRouter()

service = BookService()

LIVRE_URL = "/livres"


@router.post(LIVRE_URL, dependencies=[Depends(verify_token)])
def add(payload: LivreModel):
    inserted_model = service.add_model(payload)
    return inserted_model


@router.put(f"{LIVRE_URL}/{{_id}}", dependencies=[Depends(verify_token)])
def update(_id: str, payload: LivreModel):
    updated = service.update_model(_id, payload)

    if not updated:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found or not updated"
        )

    return updated


@router.get(LIVRE_URL, dependencies=[Depends(verify_token)])
def get_all(query_params: dict = {}):
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return models


@router.get(f"{LIVRE_URL}/{{_id}}", dependencies=[Depends(verify_token)])
def get_by_id(_id: str):
    result = service.get_model(_id)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )

    return result

@router.delete(f"{LIVRE_URL}/{{_id}}", status_code=HTTPStatus.NO_CONTENT, dependencies=[Depends(verify_token)])
def delete(_id: str):
    success = service.delete_model(_id)

    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found"
        )

    return None
