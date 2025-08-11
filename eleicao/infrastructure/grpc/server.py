from concurrent import futures
import grpc

from infrastructure.grpc.eleicao_servicer import EleicaoServicer
from app.services.eleicao_service import EleicaoService
from infrastructure.repositories.eleicao_repository_db import EleicaoRepositoryDB

from infrastructure.grpc.cargo_servicer import CargoServicer
from app.services.cargo_service import CargoService
from infrastructure.repositories.cargo_repository_db import CargoRepositoryDB

from infrastructure.grpc.candidato_servicer import CandidatoServicer
from app.services.candidato_service import CandidatoService
from infrastructure.repositories.candidato_repository_db import CandidatoRepositoryDB

from infrastructure.grpc.generated import eleicao_pb2, eleicao_pb2_grpc
from infrastructure.grpc.generated import cargo_pb2, cargo_pb2_grpc
from infrastructure.grpc.generated import candidato_pb2, candidato_pb2_grpc

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    
    eleicao_repository = EleicaoRepositoryDB()
    eleicao_service = EleicaoService(eleicao_repository)
    servicer = EleicaoServicer(eleicao_service)
    eleicao_pb2_grpc.add_EleicaoServiceServicer_to_server(servicer, server)
    
    # Cargo
    cargo_repo = CargoRepositoryDB()
    cargo_service = CargoService(cargo_repo)
    cargo_servicer = CargoServicer(cargo_service)
    cargo_pb2_grpc.add_CargoServiceServicer_to_server(cargo_servicer, server)

    # Candidato
    candidato_repo = CandidatoRepositoryDB()
    candidato_service = CandidatoService(candidato_repo, cargo_repo)
    candidato_servicer = CandidatoServicer(candidato_service)
    candidato_pb2_grpc.add_CandidatoServiceServicer_to_server(candidato_servicer, server)


    
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC rodando em localhost:50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()