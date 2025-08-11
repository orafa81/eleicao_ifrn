from domain.entities.eleicao import Eleicao, StatusEleicao
from domain.exceptions import BusinessException
from datetime import datetime
import uuid

class EleicaoService:
    def __init__(self, eleicao_repository):
        self.eleicao_repository = eleicao_repository

    def get_eleicao(self, eleicao_id: str):
        return self.eleicao_repository.get_by_id(eleicao_id)

    def create_eleicao(self, titulo: str, descricao: str, data_start: datetime, data_final: datetime):
        if not titulo or titulo.strip() == "":
            raise BusinessException("O título da eleição é obrigatório")
        
        if self.eleicao_repository.exists_by_titulo(titulo):
            raise BusinessException("Já existe uma eleição com este título")
        
        if data_start >= data_final:
            raise BusinessException("Data de início deve ser antes da data final")

        eleicao = Eleicao(
            id=str(uuid.uuid4()),
            titulo=titulo,
            descricao=descricao,
            data_start=data_start,
            data_final=data_final,
            status=StatusEleicao.AGENDADA
        )
        
        self.eleicao_repository.save(eleicao)

        return eleicao

    def edit_eleicao(self, eleicao_id: str, titulo: str, descricao: str, data_start: datetime, data_final: datetime, status: str):
        eleicao = self.eleicao_repository.get_by_id(eleicao_id)

        if not eleicao:
            raise BusinessException("Eleição não encontrada")
        
        if not titulo or titulo.strip() == "":
            raise BusinessException("O título da eleição é obrigatório")
        

        if data_start >= data_final:
            raise BusinessException("Data de início deve ser antes da data final")
        
        if eleicao.status == StatusEleicao.EM_ANDAMENTO or eleicao.status == StatusEleicao.FINALIZADA:
            raise BusinessException("Eleiçao esta em andamento, portanto não pode ser editada")
        
        eleicao.titulo = titulo
        eleicao.descricao = descricao
        eleicao.data_start = data_start
        eleicao.data_final = data_final
        eleicao.status = status

        self.eleicao_repository.save(eleicao)
        
        return eleicao
    
    def delete_eleicao(self, eleicao_id: str):
        eleicao = self.eleicao_repository.get_by_id(eleicao_id)
        
        if not eleicao:
            raise BusinessException("Eleição não encontrada")
        
        if eleicao.status == StatusEleicao.EM_ANDAMENTO or eleicao.status == StatusEleicao.FINALIZADA:
            raise BusinessException("Eleiçao esta em andamento, portanto não pode ser deletada")
        
        self.eleicao_repository.delete_by_id(eleicao_id)
        
    def list_eleicoes(self):
        return self.eleicao_repository.list_all()