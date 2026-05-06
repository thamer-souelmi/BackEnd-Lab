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


from fastapi import Depends, HTTPException

@router.get(LIVRE_URL, dependencies=[Depends(verify_token)])
def get_all(
    page: int = 1,
    limit: int = 10,
    auteur: str = None,
    annee: int = None
):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")

    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")

    return service.get_all_models(
        page=page,
        limit=limit,
        auteur=auteur,
        annee=annee
    )


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
