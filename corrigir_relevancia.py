import pandas as pd

ARQUIVO_ENTRADA = "dataset_medicamentos.csv"
ARQUIVO_SAIDA = "dataset_medicamentos.csv"

df = pd.read_csv(ARQUIVO_ENTRADA)

df["preco_numero"] = pd.to_numeric(df["preco_numero"], errors="coerce")
df["medicamento"] = df["medicamento"].astype(str).str.lower().str.strip()
df["titulo"] = df["titulo"].astype(str).str.lower().str.strip()

def calcular_relevancia(linha):
    medicamento = linha["medicamento"]
    titulo = linha["titulo"]
    preco = linha["preco_numero"]

    # Se o nome do medicamento não aparece no título, não é relevante
    if medicamento not in titulo:
        return 0

    # Se não tem preço, não é relevante
    if pd.isna(preco):
        return 0

    # Calcula preço médio daquele medicamento
    preco_medio = df[df["medicamento"] == medicamento]["preco_numero"].mean()

    # Se o preço está até a média do medicamento, é relevante
    if preco <= preco_medio:
        return 1

    return 0

df["relevante"] = df.apply(calcular_relevancia, axis=1)

df.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")

print("Coluna relevante recalculada com sucesso!")
print(df["relevante"].value_counts())