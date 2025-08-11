from infrastructure.repositories.cargo_repository_db import CargoRepositoryDB
from app.services.cargo_service import CargoService


def test_create_e_get_cargo():
    repo = CargoRepositoryDB()
    service = CargoService(repo)

    cargo = service.create_cargo("Presidente")
    assert cargo.id
    assert service.get_cargo(cargo.id).nome == "Presidente"
