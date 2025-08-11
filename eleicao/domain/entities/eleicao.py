from enum import Enum
from datetime import datetime

class StatusEleicao(str, Enum):
    AGENDADA = 'AGENDADA'
    EM_ANDAMENTO = 'EM_ANDAMENTO'
    FINALIZADA = 'FINALIZADA'

class Eleicao:
    def __init__(self, id: str, titulo: str, descricao: str, data_start: datetime, data_final: datetime, status: StatusEleicao):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data_start = data_start
        self.data_final = data_final
        self.status = status
        

   