from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from usuarios.models import User
from auth.utils import pwd_context

router = APIRouter(prefix="/auth", tags=["Login"])

class LoginInput(BaseModel):
    email: EmailStr
    senha: str

@router.post("/login")
def login(data: LoginInput, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == data.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="E-mail não cadastrado.")

    if not pwd_context.verify(data.senha, usuario.senha):
        raise HTTPException(status_code=400, detail="Senha incorreta.")

    return {"mensagem": "Login efetuado com sucesso."}
