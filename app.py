from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MediAlert AM API",
    description="API de predição de relevância de medicamentos",
    version="1.0"
)


class MedicamentoInput(BaseModel):
    medicamento: str
    farmacia: str
    localizacao: str
    categoria_preco: str


@app.get("/saude")
def saude():
    return {
        "status": "online",
        "projeto": "MediAlert AM"
    }


@app.post("/predict")
def predict(dados: MedicamentoInput):

    # Simulação inicial
    # Depois vamos ligar ao Random Forest

    if dados.categoria_preco.lower() == "baixo":
        resultado = 1
    else:
        resultado = 0

    return {
        "medicamento": dados.medicamento,
        "relevante": resultado
    }