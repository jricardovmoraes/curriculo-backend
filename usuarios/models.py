from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    cpf = Column(String)
    endereco = Column(String)
    email_confirmado = Column(Boolean, default=False)
    data_registro = Column(DateTime, default=datetime.utcnow)