from modules.schema import livre_schema
from modules.livres import LivreModel
from config.database import mongo_client
from bson import ObjectId


class BookService:
    def __init__(self):
        self.schema = livre_schema
        self.collection = mongo_client["livres"]

    def get_all_models(self, page=1, limit=10, auteur=None, annee=None):
        query = {}

        # 🔎 Filtering
        if auteur:
            query["auteur"] = {"$regex": auteur, "$options": "i"}  # case-insensitive

        if annee:
            query["annee"] = annee

        # 📄 Pagination
        skip = (page - 1) * limit

        cursor = self.collection.find(query).skip(skip).limit(limit)
        total = self.collection.count_documents(query)

        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])  # convert ObjectId → string
            results.append(LivreModel.model_validate(doc))

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total // limit) + (1 if total % limit else 0),
            "results": results
        }

    def add_model(self, model: LivreModel):
        serialized_data = model.model_dump(exclude_none=True)
        result = self.collection.insert_one(serialized_data)
        inserted_id = result.inserted_id
        return self.get_model(inserted_id)

    def get_model(self, _id):
        result = self.collection.find_one({"_id": ObjectId(_id)})

        if not result:
            return None

        # 🔥 FIX: convert ObjectId → string
        result["_id"] = str(result["_id"])

        return LivreModel.model_validate(result)


    def update_model(self, _id: str, model: LivreModel):

        data = model.model_dump(exclude_none=True)

        # never update _id
        data.pop("_id", None)
        data.pop("id", None)

        result = self.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": data}
        )

        if result.matched_count == 0:
            return None

        return self.get_model(_id)


    def delete_model(self, _id: str):

        result = self.collection.delete_one({"_id": ObjectId(_id)})

        return result.deleted_count > 0