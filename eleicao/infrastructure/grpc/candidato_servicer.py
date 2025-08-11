import grpc
from infrastructure.grpc.generated import candidato_pb2, candidato_pb2_grpc

class CandidatoServicer(candidato_pb2_grpc.CandidatoServiceServicer):
    def __init__(self, candidato_service):
        self.candidato_service = candidato_service

    def CreateCandidato(self, request, context):
        try:
            candidato = self.candidato_service.create_candidato(
                nome=request.nome,
                numero=request.numero,
                cargo_id=request.cargo_id
            )
            return candidato_pb2.CandidatoResponse(
                id=candidato.id,
                nome=candidato.nome,
                numero=candidato.numero,
                cargo_id=candidato.cargo_id
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return candidato_pb2.CandidatoResponse()

    def GetCandidato(self, request, context):
        candidato = self.candidato_service.get_candidato(request.id)
        if not candidato:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Candidato não encontrado")
            return candidato_pb2.CandidatoResponse()
        return candidato_pb2.CandidatoResponse(
            id=candidato.id,
            nome=candidato.nome,
            numero=candidato.numero,
            cargo_id=candidato.cargo_id
        )
