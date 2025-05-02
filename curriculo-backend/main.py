from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
import openai
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Buscar a API Key do .env
api_key = os.getenv("OPENAI_API_KEY")

# Inicializar o client OpenAI
client = openai.OpenAI(api_key=api_key)

app = FastAPI()

# Configurar CORS liberado para todos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Agora liberamos todas as origens para evitar travamentos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Criar o prompt para o OpenAI
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

    # Fazer a chamada para OpenAI
    response = client.chat.completions.create(
        model="gpt-4",  # ou "gpt-3.5-turbo" se quiser
        messages=[
            {"role": "system", "content": "Você é um consultor de RH especializado em recrutamento."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000
    )

    resposta_texto = response.choices[0].message.content

    return {
        "nome_arquivo": file.filename,
        "tamanho_bytes": len(conteudo),
        "conteudo_texto": texto_curriculo[:5000],
        "vaga_texto": vaga,
        "analise_openai": resposta_texto
    }
