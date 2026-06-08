import pandas as pd
import matplotlib.pyplot as plt


# ==========================
# CARREGAR DATASET
# ==========================

df = pd.read_csv("dataset_medicamentos.csv")

print("=" * 60)
print("CRISP-DM - DATA UNDERSTANDING")
print("=" * 60)

print("\nQuantidade de linhas e colunas:")
print(df.shape)

print("\nPrimeiras linhas:")
print(df.head())

print("\nTipos de dados:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

print("\nDuplicados antes da limpeza:")
print(df.duplicated().sum())


# ==========================
# DATA PREPARATION
# ==========================

print("\n" + "=" * 60)
print("CRISP-DM - DATA PREPARATION")
print("=" * 60)

df["medicamento"] = df["medicamento"].astype(str).str.lower().str.strip()
df["localizacao"] = df["localizacao"].astype(str).str.strip()
df["farmacia"] = df["farmacia"].astype(str).str.strip()
df["titulo"] = df["titulo"].astype(str).str.strip()
df["categoria_preco"] = df["categoria_preco"].astype(str).str.strip()

if "relevante" in df.columns:
    df["relevante"] = df["relevante"].fillna(0).astype(int)

linhas_antes = len(df)

df = df.drop_duplicates(
    subset=[
        "medicamento",
        "localizacao",
        "farmacia",
        "titulo",
        "link"
    ]
)

linhas_depois = len(df)

print(f"\nLinhas antes da limpeza: {linhas_antes}")
print(f"Linhas depois da limpeza: {linhas_depois}")


# ==========================
# EDA
# ==========================

print("\n" + "=" * 60)
print("EDA - ANÁLISE EXPLORATÓRIA")
print("=" * 60)

print("\nProdutos por farmácia:")
print(df["farmacia"].value_counts())

print("\nTop 10 medicamentos mais coletados:")
print(df["medicamento"].value_counts().head(10))

print("\nTop 10 localizações mais consultadas:")
print(df["localizacao"].value_counts().head(10))

print("\nCategoria de preço:")
print(df["categoria_preco"].value_counts())

if "relevante" in df.columns:
    print("\nDistribuição da variável alvo relevante:")
    print(df["relevante"].value_counts())


# ==========================
# GRÁFICO 1 - FARMÁCIAS
# ==========================

plt.figure(figsize=(8, 5))
df["farmacia"].value_counts().plot(kind="bar")
plt.title("Quantidade de Produtos por Farmácia")
plt.xlabel("Farmácia")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_farmacias.png")
plt.close()


# ==========================
# GRÁFICO 2 - MEDICAMENTOS
# ==========================

plt.figure(figsize=(10, 5))
df["medicamento"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Medicamentos Mais Coletados")
plt.xlabel("Medicamento")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_medicamentos.png")
plt.close()


# ==========================
# GRÁFICO 3 - LOCALIZAÇÕES
# ==========================

plt.figure(figsize=(10, 5))
df["localizacao"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Localizações Mais Consultadas")
plt.xlabel("Localização")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_localizacoes.png")
plt.close()


# ==========================
# GRÁFICO 4 - CATEGORIA DE PREÇO
# ==========================

plt.figure(figsize=(8, 5))
df["categoria_preco"].value_counts().plot(kind="bar")
plt.title("Distribuição por Categoria de Preço")
plt.xlabel("Categoria de Preço")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_categoria_preco.png")
plt.close()


# ==========================
# GRÁFICO 5 - RELEVÂNCIA
# ==========================

if "relevante" in df.columns:
    plt.figure(figsize=(6, 5))
    df["relevante"].value_counts().plot(kind="bar")
    plt.title("Distribuição da Variável Alvo: Relevante")
    plt.xlabel("Relevante")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.savefig("grafico_relevancia.png")
    plt.close()


# ==========================
# GRÁFICO 6 - HISTOGRAMA DE PREÇOS
# ==========================

if "preco_numero" in df.columns:
    df_precos = df.dropna(subset=["preco_numero"])

    if len(df_precos) > 0:
        plt.figure(figsize=(10, 5))
        df_precos["preco_numero"].hist(bins=20)
        plt.title("Distribuição dos Preços Coletados")
        plt.xlabel("Preço")
        plt.ylabel("Frequência")
        plt.tight_layout()
        plt.savefig("grafico_histograma_precos.png")
        plt.close()


# ==========================
# SALVAR DATASET LIMPO
# ==========================

df.to_csv(
    "dataset_medicamentos_limpo.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 60)
print("ARQUIVOS GERADOS")
print("=" * 60)

print("dataset_medicamentos_limpo.csv")
print("grafico_farmacias.png")
print("grafico_medicamentos.png")
print("grafico_localizacoes.png")
print("grafico_categoria_preco.png")
print("grafico_relevancia.png")
print("grafico_histograma_precos.png")

print("\nEDA finalizada com sucesso!")