from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from auth.schemas import UserCreate
from usuarios.models import User
from auth.utils import hash_password, send_confirmation_email
from database import get_db
from fastapi import status

import re

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in [9, 10]:
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if int(cpf[i]) != digito:
            return False

    return True



router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Valida CPF
    if not validar_cpf(user.cpf):
        raise HTTPException(status_code=400, detail="CPF inválido.")

    # Verifica se e-mail já está em uso
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # Criptografa a senha
    hashed_password = hash_password(user.senha)

    # Cria novo usuário
    new_user = User(
        nome=user.nome,
        email=user.email,
        senha=hashed_password,
        cpf=user.cpf,
        endereco=user.endereco,
        email_confirmado=False,
        data_registro=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Envia e-mail de confirmação (simulado)
    send_confirmation_email(user.email)

    from fastapi import status

    return {"mensagem": "Usuário registrado com sucesso. Verifique seu e-mail."}


