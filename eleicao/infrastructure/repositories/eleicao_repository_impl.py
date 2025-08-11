from domain.entities.eleicao import Eleicao, StatusEleicao
from domain.repositories.eleicao_repository import EleicaoRepository
from datetime import datetime

class InMemoryEleicaoRepository(EleicaoRepository):
    def __init__(self):
        self.eleicoes = {}
        
    def get_by_id(self, eleicao_id: str):
        return self.eleicoes.get(eleicao_id)
    
    def list_all(self):
        return list(self.eleicoes.values())
    
    def delete_by_id(self, eleicao_id: str):
        if eleicao_id in self.eleicoes:
            del self.eleicoes[eleicao_id]

    def save(self, eleicao):
        self.eleicoes[eleicao.id] = eleicao

    def exists_by_titulo(self, titulo: str) -> bool:
        return any(e.titulo == titulo for e in self.eleicoes.values())