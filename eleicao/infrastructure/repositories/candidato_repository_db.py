from infrastructure.database import SessionLocal
from infrastructure.models.candidato_model import CandidatoModel
from domain.entities.candidato import Candidato

class CandidatoRepositoryDB:
    def save(self, candidato: Candidato):
        with SessionLocal() as session:
            model = CandidatoModel(
                id=candidato.id,
                nome=candidato.nome,
                numero=candidato.numero,
                cargo_id=candidato.cargo_id,
            )
            session.merge(model)
            session.commit()

    def get_by_id(self, id: str):
        with SessionLocal() as session:
            model = session.query(CandidatoModel).filter_by(id=id).first()
            return self._to_entity(model) if model else None

    def get_all(self):
        with SessionLocal() as session:
            models = session.query(CandidatoModel).all()
            return [self._to_entity(m) for m in models]

    def delete(self, id: str):
        with SessionLocal() as session:
            model = session.query(CandidatoModel).filter_by(id=id).first()
            if model:
                session.delete(model)
                session.commit()

    def _to_entity(self, model: CandidatoModel):
        return Candidato(
            id=model.id,
            nome=model.nome,
            numero=model.numero,
            cargo_id=model.cargo_id,
        )
