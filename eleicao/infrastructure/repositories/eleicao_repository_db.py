from infrastructure.database import SessionLocal
from infrastructure.models.eleicao_model import EleicaoModel
from domain.entities.eleicao import Eleicao

class EleicaoRepositoryDB:
    def save(self, eleicao: Eleicao):
        with SessionLocal() as session:
            model = EleicaoModel(
                id=eleicao.id,
                titulo=eleicao.titulo,
                descricao=eleicao.descricao,
                data_start=eleicao.data_start,
                data_final=eleicao.data_final,
                status=eleicao.status
            )
            session.merge(model)
            session.commit()

    def get_by_id(self, id: str):
        with SessionLocal() as session:
            model = session.query(EleicaoModel).filter_by(id=id).first()
            return self._to_entity(model) if model else None

    def get_all(self):
        with SessionLocal() as session:
            models = session.query(EleicaoModel).all()
            return [self._to_entity(m) for m in models]

    def delete(self, id: str):
        with SessionLocal() as session:
            model = session.query(EleicaoModel).filter_by(id=id).first()
            if model:
                session.delete(model)
                session.commit()

    def exists_by_titulo(self, titulo: str) -> bool:
        with SessionLocal() as session:
            return session.query(
                session.query(EleicaoModel).filter_by(titulo=titulo).exists()
            ).scalar()
        
    def _to_entity(self, model: EleicaoModel):
        return Eleicao(
            id=model.id,
            titulo=model.titulo,
            descricao=model.descricao,
            data_start=model.data_start,
            data_final=model.data_final,
            status=model.status
        )
