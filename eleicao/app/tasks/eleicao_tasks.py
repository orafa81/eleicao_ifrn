from celery import Celery
from datetime import datetime
from app.services.eleicao_service import EleicaoService
from infrastructure.repositories.eleicao_repository_impl import InMemoryEleicaoRepository

app = Celery("eleicao", broker="redis://localhost:6379/0")

eleicao_repository = InMemoryEleicaoRepository()
eleicao_service = EleicaoService(eleicao_repository)

@app.task
def iniciar_eleicao_task(eleicao_id):
    eleicao = eleicao_repository.get_by_id(eleicao_id)
    if eleicao and eleicao.status == "AGENDADA":
        eleicao.status = "EM_ANDAMENTO"
        eleicao_repository.save(eleicao)
        print(f"[{datetime.now()}] ✅ Eleição {eleicao_id} iniciada.")

@app.task
def finalizar_eleicao_task(eleicao_id):
    eleicao = eleicao_repository.get_by_id(eleicao_id)
    if eleicao and eleicao.status == "EM_ANDAMENTO":
        eleicao.status = "FINALIZADA"
        eleicao_repository.save(eleicao)
        print(f"[{datetime.now()}] ✅ Eleição {eleicao_id} finalizada.")
