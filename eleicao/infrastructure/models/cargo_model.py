from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database import Base

class CargoModel(Base):
    __tablename__ = "cargos"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    eleicao_id = Column(String, ForeignKey("eleicoes.id"), nullable=False)

    eleicao = relationship("EleicaoModel", back_populates="cargos")
    candidatos = relationship("CandidatoModel", back_populates="cargo", cascade="all, delete-orphan")