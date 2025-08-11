from infrastructure.database import SessionLocal
from infrastructure.models.cargo_model import CargoModel
from domain.entities.cargo import Cargo

class CargoRepositoryDB:
    def save(self, cargo: Cargo):
        with SessionLocal() as session:
            model = CargoModel(
                id=cargo.id,
                nome=cargo.nome,
                eleicao_id=cargo.eleicao_id
            )
            session.merge(model)
            session.commit()

    def get_by_id(self, id: str):
        with SessionLocal() as session:
            model = session.query(CargoModel).filter_by(id=id).first()
            return self._to_entity(model) if model else None

    def get_all(self):
        with SessionLocal() as session:
            models = session.query(CargoModel).all()
            return [self._to_entity(m) for m in models]

    def delete(self, id: str):
        with SessionLocal() as session:
            model = session.query(CargoModel).filter_by(id=id).first()
            if model:
                session.delete(model)
                session.commit()

    def _to_entity(self, model: CargoModel):
        return Cargo(
            id=model.id,
            nome=model.nome,
            eleicao_id=model.eleicao_id
        )
