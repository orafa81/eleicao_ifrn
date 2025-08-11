class InMemoryCargoRepository:
    def __init__(self):
        self.db = {}

    def save(self, cargo):
        self.db[cargo.id] = cargo

    def get_by_id(self, cargo_id):
        return self.db.get(cargo_id)