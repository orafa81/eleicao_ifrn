from domain.entities.candidato import Candidato
import uuid

class CandidatoService:
    def __init__(self, repository, cargo_repository):
        self.repository = repository
        self.cargo_repository = cargo_repository

    def create_candidato(self, nome : str, numero : int, cargo_id : str):
        if not self.cargo_repository.get_by_id(cargo_id):
            raise Exception("Cargo não encontrado")
        
        candidato = Candidato(
            id=str(uuid.uuid4()),
            nome=nome, 
            numero=numero, 
            cargo_id=cargo_id
        )
        
        self.repository.save(candidato)
        
        return candidato

    def get_candidato(self, candidato_id):
        return self.repository.get_by_id(candidato_id)