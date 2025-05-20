from usuarios.models import User
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
import pdfplumber
import io
import openai
from dotenv import load_dotenv
import os
from database import engine, Base
from auth.routes import router as auth_router
from auth.login import router as login_router

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(title="SmartCV - Currículo Inteligente")

# Configurar CORS (liberado para todos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas de autenticação e login
app.include_router(auth_router)
app.include_router(login_router)

@app.get("/")
def read_root():
    return {"mensagem": "Back-end do Currículo Inteligente rodando com segurança!"}

@app.post("/upload-curriculo/")
async def upload_curriculo(file: UploadFile = File(...), vaga: str = Form(...)):
    conteudo = await file.read()
    texto_curriculo = ""

    if file.content_type == "application/pdf":
        with pdfplumber.open(io.BytesIO(conteudo)) as pdf:
            for pagina in pdf.pages:
                texto_curriculo += pagina.extract_text() or ""
    else:
        texto_curriculo = "Formato de arquivo não suportado ainda."

    prompt = f"""
Você é um especialista em recrutamento e seleção.

Receba o currículo de um candidato e a descrição de uma vaga.

Analise se o candidato é aderente à vaga e responda:

- O candidato é adequado? (Sim ou Não)
- Principais pontos fortes.
- Pontos fracos ou lacunas.
- Sugestões para melhorar o currículo.

Currículo:
{texto_curriculo}

Vaga:
{vaga}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um consultor de RH especializado em recrutamento."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    resposta_texto = response.choices[0].message.content

    return {
        "nome_arquivo": file.filename,
        "tamanho_bytes": len(conteudo),
        "conteudo_texto": texto_curriculo[:5000],
        "vaga_texto": vaga,
        "analise_openai": resposta_texto
    }
