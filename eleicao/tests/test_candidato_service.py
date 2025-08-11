import pytest
from infrastructure.repositories.cargo_repository_db import CargoRepositoryDB
from app.services.cargo_service import CargoService
from domain.entities.cargo import Cargo

from infrastructure.repositories.candidato_repository_db import CandidatoRepositoryDB
from app.services.candidato_service import CandidatoService

def test_create_candidato_com_cargo_valido():
    cargo_repo = CargoRepositoryDB()
    service = CargoService(cargo_repo)

    cargo = service.create_cargo("Presidente")

    repo = CandidatoRepositoryDB()
    service = CandidatoService(repo, cargo_repo)

    candidato = service.create_candidato("João", 45, cargo.id)
    assert candidato.nome == "João"

def test_candidato_com_cargo_inexistente_lanca_erro():
    repo = CandidatoRepositoryDB()
    service = CandidatoService(repo, CargoRepositoryDB())

    with pytest.raises(Exception):
        service.create_candidato("Zé", 13, "cargo-fake")