# from fastapi import APIRouter, HTTPException
#
# from modules.service import BookService
# from modules.livres import LivreModel, LivrePatchModel
# from common.helpers.filters import Filters
#
# router = APIRouter(prefix="/livres", tags=["Livres"])
#
# service = BookService()
#
# #
# # def creer_livre(db: Session, data):
# #     livre = Livre(**data.dict())
# #     db.add(livre)
# #     db.commit()
# #     db.refresh(livre)
# #     return livre
# #
# #
# # def obtenir_livres(db: Session):
# #     return db.query(Livre).all()
# #
# #
# # def obtenir_livre(db: Session, livre_id: int):
# #     return db.get(Livre, livre_id)
# #
# #
# # def modifier_livre(db: Session, livre, data):
# #     for cle, valeur in data.dict(exclude_unset=True).items():
# #         setattr(livre, cle, valeur)
# #
# #     db.commit()
# #     db.refresh(livre)
# #     return livre
# #
# #
# # def supprimer_livre(db: Session, livre):
# #     db.delete(livre)
# #     db.commit()