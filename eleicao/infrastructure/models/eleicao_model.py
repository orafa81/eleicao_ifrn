from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from infrastructure.database import Base
import enum

class StatusEnum(str, enum.Enum):
    EM_ANDAMENTO = 'EM_ANDAMENTO'
    FINALIZADA = 'FINALIZADA'
    AGUARDANDO = "AGENDADA"

class EleicaoModel(Base):
    __tablename__ = "eleicoes"

    id = Column(String, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    data_start = Column(DateTime, nullable=False)
    data_final = Column(DateTime, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)

    cargos = relationship("CargoModel", back_populates="eleicao", cascade="all, delete-orphan")