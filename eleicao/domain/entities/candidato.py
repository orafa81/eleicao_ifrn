from domain.entities.cargo import Cargo

class Candidato:
    def __init__(self, id: str, numero: int, nome: str, cargo_id: str):
        self.id = id
        self.numero = numero
        self.nome = nome
        self.cargo_id = cargo_id
        
