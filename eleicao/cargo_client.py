import grpc
from datetime import datetime

from infrastructure.grpc.generated import cargo_pb2, cargo_pb2_grpc


def create_cargo(stub,  eleicao_id):
    print("\n📦 Criando novo cargo...")
    print(f"[DEBUG] CargoService.create_cargo chamado com eleicao_id: '{eleicao_id}'")
    request = cargo_pb2.CreateCargoRequest(
        nome="Presidente",
        eleicao_id=eleicao_id
    )
    response = stub.CreateCargo(request)
    print(f"✅ Cargo criado com ID: {response.id}")
    return response.id


def get_cargo(stub, cargo_id):
    print(f"\n🔍 Buscando cargo com ID: {cargo_id}")

    request = cargo_pb2.GetCargoRequest(id=cargo_id)
    try:
        response = stub.GetCargo(request)
        print(f"✅ Cargo encontrado: {response.nome}")
    except grpc.RpcError as e:
        print("❌ Erro ao buscar cargo:", e.details())


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = cargo_pb2_grpc.CargoServiceStub(channel)

        eleicao_id = "e96054cd-2c0b-4bf6-bdbe-19571d5bf222"  

        cargo_id = create_cargo(stub, eleicao_id)
        get_cargo(stub, cargo_id)

if __name__ == "__main__":
    run()
