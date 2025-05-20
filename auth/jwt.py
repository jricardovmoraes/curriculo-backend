from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from usuarios.models import User
from auth.utils import pwd_context
from auth.jwt import criar_token, verificar_token

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

    token = criar_token({"sub": str(usuario.id), "email": usuario.email})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def me(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou malformado")

    token = authorization.split(" ")[1]
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    usuario = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "cpf": usuario.cpf,
        "endereco": usuario.endereco,
        "data_registro": usuario.data_registro,
    }
