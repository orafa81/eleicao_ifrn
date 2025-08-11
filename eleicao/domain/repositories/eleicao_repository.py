from abc import ABC, abstractmethod

class EleicaoRepository(ABC):
    @abstractmethod
    def get_by_id(self, eleicao_id: str):
        pass
    
    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def delete_by_id(self, eleicao_id: str):
        pass

    @abstractmethod
    def exists_by_titulo(self, titulo: str) -> bool:
        pass
    
    @abstractmethod
    def save(self, eleicao):
        pass
    
    