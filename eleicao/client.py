import grpc
from datetime import datetime
from infrastructure.grpc.generated import eleicao_pb2, eleicao_pb2_grpc

def create_eleicao(stub):
    print("➡️ Criando uma nova eleição...")
    request = eleicao_pb2.CreateEleicaoRequest(
        titulo="Mais uma Eleicao Teste 10",
        descricao="Criada pelo client gRPC",
        data_start=datetime(2025, 7, 1).isoformat(),
        data_final=datetime(2025, 7, 10).isoformat()
    )

    try:
        response = stub.CreateEleicao(request)
        print("✅ Eleição criada com sucesso:")
        print(f"ID: {response.id}")
        print(f"Título: {response.titulo}")
        print(f"Status: {response.status}")
        return response.id  # Retorna o ID para buscar depois
    except grpc.RpcError as e:
        print("❌ Erro ao criar eleição:")
        print(f"Status: {e.code().name}")
        print(f"Detalhes: {e.details()}")
        return None

def get_eleicao(stub, eleicao_id):
    print(f"\n🔍 Buscando eleição com ID: {eleicao_id}")
    request = eleicao_pb2.EleicaoRequest(id=eleicao_id)

    try:
        response = stub.GetEleicao(request)
        print("✅ Eleição encontrada:")
        print(f"ID: {response.id}")
        print(f"Título: {response.titulo}")
        print(f"Descrição: {response.descricao}")
        print(f"Data Início: {response.data_start}")
        print(f"Data Final: {response.data_final}")
        print(f"Status: {response.status}")
    except grpc.RpcError as e:
        print("❌ Erro ao buscar eleição:")
        print(f"Status: {e.code().name}")
        print(f"Detalhes: {e.details()}")

def edit_eleicao(stub, eleicao_id):
    print(f"\n✏️ Editando eleição com ID: {eleicao_id}")

    request = eleicao_pb2.EditEleicaoRequest(
        id=eleicao_id,
        titulo="Eleição Editada via Client",
        descricao="Agora com nova descrição",
        data_start=datetime(2025, 7, 5).isoformat(),
        data_final=datetime(2025, 7, 15).isoformat(),
        status="EM_ANDAMENTO"
    )

    try:
        response = stub.EditEleicao(request)
        print("✅ Eleição editada com sucesso:")
        print(f"ID: {response.id}")
        print(f"Título: {response.titulo}")
        print(f"Status: {response.status}")
    except grpc.RpcError as e:
        print("❌ Erro ao editar eleição:")
        print(f"Status: {e.code().name}")
        print(f"Detalhes: {e.details()}")
        
def delete_eleicao(stub, eleicao_id):
    print(f"\n🗑️ Deletando eleição com ID: {eleicao_id}")

    request = eleicao_pb2.DeleteEleicaoRequest(id=eleicao_id)
    try:
        response = stub.DeleteEleicao(request)
        print("✅", response.message)
    except grpc.RpcError as e:
        print("❌ Erro ao deletar eleição:")
        print(f"Status: {e.code().name}")
        print(f"Detalhes: {e.details()}")
        
def list_eleicoes(stub):
    print("\n📋 Listando todas as eleições...")

    request = eleicao_pb2.ListEleicoesRequest()
    try:
        response = stub.ListEleicoes(request)
        if not response.eleicoes:
            print("⚠️ Nenhuma eleição cadastrada.")
        for e in response.eleicoes:
            print(f"- {e.id} | {e.titulo} | {e.status}")
    except grpc.RpcError as e:
        print("❌ Erro ao listar eleições:")
        print(f"Status: {e.code().name}")
        print(f"Detalhes: {e.details()}")

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = eleicao_pb2_grpc.EleicaoServiceStub(channel)
        
        # 1. Cria a eleição
        eleicao_id = create_eleicao(stub)
        
        #2. Busca a eleição
        if eleicao_id:
            get_eleicao(stub, eleicao_id)
            #delete_eleicao(stub, eleicao_id)
            #get_eleicao(stub, eleicao_id)
            
        # list_eleicoes(stub)

if __name__ == "__main__":
    run()
