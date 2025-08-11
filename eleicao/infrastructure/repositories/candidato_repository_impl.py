class InMemoryCandidatoRepository:
    def __init__(self):
        self.db = {}

    def save(self, candidato):
        self.db[candidato.id] = candidato

    def get_by_id(self, candidato_id):
        return self.db.get(candidato_id)