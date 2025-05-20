from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    nome: constr(min_length=2)
    email: EmailStr
    senha: constr(min_length=6)
    cpf: constr(min_length=11, max_length=14)
    endereco: str
