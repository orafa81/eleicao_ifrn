from app.tasks.eleicao_tasks import iniciar_eleicao_task, finalizar_eleicao_task
from infrastructure.grpc.generated import eleicao_pb2, eleicao_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

class EleicaoServicer(eleicao_pb2_grpc.EleicaoServiceServicer):
    def __init__(self, eleicao_service):
        self.eleicao_service = eleicao_service

    def CreateEleicao(self, request, context):
        try:
             # ✅ Aqui convertemos as datas recebidas em strings ISO para datetime
            data_start = datetime.fromisoformat(request.data_start)
            data_final = datetime.fromisoformat(request.data_final)
            
            eleicao = self.eleicao_service.create_eleicao(
                titulo=request.titulo,
                descricao=request.descricao,
                data_start=data_start,
                data_final=data_final
            )

            iniciar_eleicao_task.apply_async((eleicao.id,), eta=data_start)
            finalizar_eleicao_task.apply_async((eleicao.id,), eta=data_final)

            
            return eleicao_pb2.CreateEleicaoResponse(
                id=eleicao.id,
                titulo=eleicao.titulo,
                status=eleicao.status
            )
        except Exception as e:
            context.set_code(3)  
            context.set_details(str(e))
            return eleicao_pb2.CreateEleicaoResponse()
    
    def EditEleicao(self, request, context):
        try:
            eleicao = self.eleicao_service.edit_eleicao(
                eleicao_id=request.id,
                titulo=request.titulo,
                descricao=request.descricao,
                data_start=datetime.fromisoformat(request.data_start),
                data_final=datetime.fromisoformat(request.data_final),
                status=request.status
            )

            return eleicao_pb2.EditEleicaoResponse(
                id=eleicao.id,
                titulo=eleicao.titulo,
                descricao=eleicao.descricao,
                data_start=eleicao.data_start.isoformat(),
                data_final=eleicao.data_final.isoformat(),
                status=eleicao.status
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return eleicao_pb2.EditEleicaoResponse()
    
    def ListEleicoes(self, request, context):
        eleicoes = self.eleicao_service.list_eleicoes()

        eleicoes_proto = [
            eleicao_pb2.EleicaoResponse(
                id=e.id,
                titulo=e.titulo,
                descricao=e.descricao,
                data_start=e.data_start.isoformat(),
                data_final=e.data_final.isoformat(),
                status=e.status
            )
            for e in eleicoes
        ]

        return eleicao_pb2.ListEleicoesResponse(eleicoes=eleicoes_proto)

        
    def DeleteEleicao(self, request, context):
        try:
            self.eleicao_service.delete_eleicao(request.id)
            return eleicao_pb2.DeleteEleicaoResponse(message="Eleição removida com sucesso.")
        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return eleicao_pb2.DeleteEleicaoResponse()
            
    def GetEleicao(self, request, context):
        eleicao = self.eleicao_service.get_eleicao(request.id)
        if eleicao is None:
            context.set_code(5)  
            context.set_details('Eleição não encontrada')
            return eleicao_pb2.EleicaoResponse()

        return eleicao_pb2.EleicaoResponse(
            id=eleicao.id,
            titulo=eleicao.titulo,
            descricao=eleicao.descricao,
            data_start=eleicao.data_start.isoformat(),
            data_final=eleicao.data_final.isoformat(),
            status=eleicao.status
        )