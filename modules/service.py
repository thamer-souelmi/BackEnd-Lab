from modules.schema import livre_schema
from modules.livres import LivreModel, LivreModelResult
from config.database import mongo_client
from bson import ObjectId
from pymongoose import methods
from common.helpers.filters import Filters


class BookService:
    def __init__(self):
        self.schema = livre_schema
        self.collection = mongo_client["livres"]

    def get_all_models(self, filters):
        query = {}  # ignore filters for now

        cursor = self.collection.find(query)

        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])  # convert ObjectId
            results.append(LivreModel.model_validate(doc))

        return LivreModelResult(
            total=len(results),
            results=results
        )

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