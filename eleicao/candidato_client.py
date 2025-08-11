import grpc
from infrastructure.grpc.generated import candidato_pb2, candidato_pb2_grpc


def create_candidato(stub, nome, numero, cargo_id):
    print(f"\n👤 Criando candidato {nome}...")

    request = candidato_pb2.CreateCandidatoRequest(
        nome=nome,
        numero=numero,
        cargo_id=cargo_id
    )
    try:
        response = stub.CreateCandidato(request)
        print(f"✅ Candidato criado: {response.nome} - Nº {response.numero}")
        return response.id
    except grpc.RpcError as e:
        print("❌ Erro ao criar candidato:", e.details())
        return None


def get_candidato(stub, candidato_id):
    print(f"\n🔍 Buscando candidato com ID: {candidato_id}")

    request = candidato_pb2.GetCandidatoRequest(id=candidato_id)
    try:
        response = stub.GetCandidato(request)
        print(f"✅ Candidato: {response.nome} - Nº {response.numero} - Cargo ID: {response.cargo_id}")
    except grpc.RpcError as e:
        print("❌ Erro ao buscar candidato:", e.details())


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = candidato_pb2_grpc.CandidatoServiceStub(channel)

        # Você pode passar um cargo_id real aqui
        cargo_id = input("Informe o ID do cargo existente para vincular ao candidato: ")
        candidato_id = create_candidato(stub, "Maria Silva", 17, cargo_id)

        if candidato_id:
            get_candidato(stub, candidato_id)


if __name__ == "__main__":
    run()
