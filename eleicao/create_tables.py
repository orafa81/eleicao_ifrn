# create_tables.py
from infrastructure.database import Base, engine
from infrastructure.models.eleicao_model import EleicaoModel
from infrastructure.models.cargo_model import CargoModel
from infrastructure.models.candidato_model import CandidatoModel

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")