from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Exemplo: usando PostgreSQL
DATABASE_URL = "postgresql+psycopg2://eleicao:admin@postgres:5432/eleicao_if"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

