import grpc
from infrastructure.grpc.generated import cargo_pb2, cargo_pb2_grpc

class CargoServicer(cargo_pb2_grpc.CargoServiceServicer):
    def __init__(self, cargo_service):
        self.cargo_service = cargo_service

    def CreateCargo(self, request, context):
        print(f"[DEBUG] CreateCargo chamado com eleicao_id: '{request.eleicao_id}'")
        cargo = self.cargo_service.create_cargo(
            nome=request.nome,
            eleicao_id=request.eleicao_id  
        )
        return cargo_pb2.CargoResponse(
            id=cargo.id,
            nome=cargo.nome,
            eleicao_id=cargo.eleicao_id
    )

    def GetCargo(self, request, context):
        cargo = self.cargo_service.get_cargo(request.id)
        if not cargo:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Cargo não encontrado")
            return cargo_pb2.CargoResponse()
        return cargo_pb2.CargoResponse(
            id=cargo.id,
            nome=cargo.nome,
        )
