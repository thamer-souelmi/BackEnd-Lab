class Filters:

    def __init__(self, **kwargs):
        self.limit = int(kwargs.get("limit", 10))  # default 10
        self.page = int(kwargs.get("page", 1))    # default page 1

        self.email = kwargs.get("email")
        self.role = kwargs.get("role")
        self.status = kwargs.get("status")
        self.teamId = kwargs.get("teamId")
        self.teamName = kwargs.get("teamName")

        self.skip = (self.page - 1) * self.limit

    def apply(self):
        query = {}

        if self.email:
            query["user.email"] = self.email

        if self.role:
            query["role"] = self.role

        if self.status:
            query["status"] = self.status

        # soft delete filter
        query["$or"] = [
            {"deletedAt": None},
            {"deletedAt": {"$exists": False}},
            {"deletedAt": ""}
        ]

        return query