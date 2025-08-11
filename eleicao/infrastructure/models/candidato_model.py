from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database import Base

class CandidatoModel(Base):
    __tablename__ = "candidatos"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    numero = Column(Integer, nullable=True)
    cargo_id = Column(String, ForeignKey("cargos.id"), nullable=False)

    cargo = relationship("CargoModel", back_populates="candidatos")
