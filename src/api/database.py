from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

# Instancia do banco de dados
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()