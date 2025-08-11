import pytest
from infrastructure.database import SessionLocal
from unittest.mock import MagicMock
from datetime import datetime
from domain.entities.eleicao import Eleicao, StatusEleicao
from domain.repositories.eleicao_repository import EleicaoRepository
from domain.exceptions import BusinessException
from app.services.eleicao_service import EleicaoService
from infrastructure.grpc.eleicao_servicer import EleicaoServicer
from infrastructure.grpc.generated import eleicao_pb2

class FakeEleicaoRepository(EleicaoRepository):
    def __init__(self):
        self.eleicoes = {}

    def get_by_id(self, eleicao_id: str):
        return self.eleicoes.get(eleicao_id)

    def save(self, eleicao: Eleicao):
        self.eleicoes[eleicao.id] = eleicao
    
    def exists_by_titulo(self, titulo: str) -> bool:
        return any(e.titulo == titulo for e in self.eleicoes.values())
    
    def delete_by_id(self, eleicao_id):
        if eleicao_id in self.eleicoes:
            del self.eleicoes[eleicao_id]

    def list_all(self):
        return list(self.eleicoes.values())

@pytest.fixture
def eleicao_service():
    return EleicaoService(FakeEleicaoRepository())

@pytest.fixture
def eleicao_mock_service():
    return MagicMock()

@pytest.fixture
def servicer(eleicao_mock_service):
    return EleicaoServicer(eleicao_service=eleicao_mock_service)

def test_deve_criar_eleicao_com_dados_validos(eleicao_service):
    titulo = "Nova Eleição"
    descricao = "Descrição teste"
    data_start = datetime(2025, 7, 1)
    data_final = datetime(2025, 7, 10)

    eleicao = eleicao_service.create_eleicao(titulo, descricao, data_start, data_final)

    assert eleicao.id is not None
    assert eleicao.titulo == titulo
    assert eleicao.status == StatusEleicao.AGENDADA

def test_nao_deve_criar_eleicao_com_datas_invalidas(eleicao_service):
    data_start = datetime(2025, 7, 10)
    data_final = datetime(2025, 7, 1)

    with pytest.raises(BusinessException):
        eleicao_service.create_eleicao(
            titulo="Eleição Inválida",
            descricao="Teste",
            data_start=data_start,
            data_final=data_final
        )

def test_nao_deve_criar_eleicao_sem_titulo(eleicao_service):
    with pytest.raises(BusinessException, match="título da eleição é obrigatório"):
        eleicao_service.create_eleicao(
            titulo="",
            descricao="Teste sem título",
            data_start=datetime(2025, 7, 1),
            data_final=datetime(2025, 7, 10)
        )

def test_nao_deve_criar_eleicao_com_titulo_repetido(eleicao_service):
    
    eleicao_service.create_eleicao(
        titulo="Eleição Unica",
        descricao="Primeira eleição",
        data_start=datetime(2025, 7, 1),
        data_final=datetime(2025, 7, 10)
    )

   
    with pytest.raises(BusinessException, match="Já existe uma eleição com este título"):
        eleicao_service.create_eleicao(
            titulo="Eleição Unica",
            descricao="Tentativa duplicada",
            data_start=datetime(2025, 8, 1),
            data_final=datetime(2025, 8, 10)
        )
def test_nao_deve_criar_eleicao_com_data_inicio_maior_que_data_final(eleicao_service):
    with pytest.raises(BusinessException, match="Data de início deve ser antes da data final"):
        eleicao_service.create_eleicao(
            titulo= "Eleicaio Unica",
            descricao="Tentativa data",
            data_start=datetime(2025, 8, 5),
            data_final=datetime(2025, 8, 1)
        )

def test_nao_deve_criar_eleicao_com_datas_invalidas(eleicao_service):
    data_start = datetime(2025, 7, 10)
    data_final = datetime(2025, 7, 1)

    with pytest.raises(BusinessException):
        eleicao_service.create_eleicao(
            titulo="Eleição Inválida",
            descricao="Teste",
            data_start=data_start,
            data_final=data_final
        )

def test_nao_deve_editar_eleicao_se_eleicao_estiver_em_andamento_finalizada(eleicao_service):
    eleicao = eleicao_service.create_eleicao(
        titulo="Eleição Teste",
        descricao="Primeira eleição",
        data_start=datetime(2025, 7, 1),
        data_final=datetime(2025, 7, 10)
    )
    eleicao.status = StatusEleicao.EM_ANDAMENTO

    with pytest.raises(BusinessException, match="Eleiçao esta em andamento, portanto não pode ser editada"):
        eleicao_service.edit_eleicao(eleicao_id = eleicao.id,
            titulo= "Eleicaio Unica",
            descricao="Tentativa data",
            data_start=datetime(2025, 8, 1),
            data_final=datetime(2025, 8, 5),
            status="FINALIZADA"
        )


def test_get_eleicao_sucesso(eleicao_service):
    # cria uma eleição para ser buscada
    eleicao = eleicao_service.create_eleicao(
        "Teste Get",
        "Descrição",
        datetime(2025, 7, 1),
        datetime(2025, 7, 10)
    )
    resultado = eleicao_service.get_eleicao(eleicao.id)
    assert resultado is not None
    assert resultado.titulo == "Teste Get"

def test_get_eleicao_nao_encontrada(eleicao_service):
    resultado = eleicao_service.get_eleicao("id-nao-existente")
    assert resultado is None