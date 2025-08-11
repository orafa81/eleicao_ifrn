from domain.entities.cargo import Cargo
import uuid

class CargoService:
    def __init__(self, repository):
        self.repository = repository

    def create_cargo(self, nome: str, eleicao_id: str):
        cargo = Cargo(
            id=str(uuid.uuid4()),
            nome=nome,
            eleicao_id=eleicao_id
        )
        self.repository.save(cargo)
        return cargo

    def get_cargo(self, cargo_id):
        return self.repository.get_by_id(cargo_id)
