from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def send_confirmation_email(email: str):
    # Simulação de envio de e-mail (substituir por lógica real com SMTP ou serviço externo)
    print(f"E-mail de confirmação enviado para: {email}")
