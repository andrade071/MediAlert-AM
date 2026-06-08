import pandas as pd
import matplotlib.pyplot as plt


<<<<<<< HEAD
# ==========================
# CARREGAR DATASET
# ==========================

df = pd.read_csv("dataset_medicamentos.csv")

print("=" * 60)
print("CRISP-DM - DATA UNDERSTANDING")
print("=" * 60)

print("\nQuantidade de linhas e colunas:")
=======
df = pd.read_csv("dataset_medicamentos.csv")

print("=" * 50)
print("CRISP-DM - DATA UNDERSTANDING")
print("=" * 50)

print("\nDimensão do dataset:")
>>>>>>> b8623c99592493d5c84f74dfda2d58e9cf026c58
print(df.shape)

print("\nPrimeiras linhas:")
print(df.head())

print("\nTipos de dados:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

<<<<<<< HEAD
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
=======
print("\nDuplicados:")
print(df.duplicated().sum())


print("\n" + "=" * 50)
print("DATA PREPARATION")
print("=" * 50)

df["medicamento"] = df["medicamento"].astype(str).str.lower().str.strip()
df["farmacia"] = df["farmacia"].astype(str).str.strip()
df["localizacao"] = df["localizacao"].astype(str).str.strip()
df["titulo"] = df["titulo"].astype(str).str.strip()

linhas_antes = len(df)
df = df.drop_duplicates()
linhas_depois = len(df)

print(f"Linhas antes da limpeza: {linhas_antes}")
print(f"Linhas depois da limpeza: {linhas_depois}")


print("\n" + "=" * 50)
print("EDA - ANÁLISE EXPLORATÓRIA")
print("=" * 50)
>>>>>>> b8623c99592493d5c84f74dfda2d58e9cf026c58

print("\nProdutos por farmácia:")
print(df["farmacia"].value_counts())

<<<<<<< HEAD
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

=======
>>>>>>> b8623c99592493d5c84f74dfda2d58e9cf026c58
plt.figure(figsize=(8, 5))
df["farmacia"].value_counts().plot(kind="bar")
plt.title("Quantidade de Produtos por Farmácia")
plt.xlabel("Farmácia")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_farmacias.png")
plt.close()


<<<<<<< HEAD
# ==========================
# GRÁFICO 2 - MEDICAMENTOS
# ==========================

plt.figure(figsize=(10, 5))
df["medicamento"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Medicamentos Mais Coletados")
=======
print("\nMedicamentos mais coletados:")
print(df["medicamento"].value_counts())

plt.figure(figsize=(8, 5))
df["medicamento"].value_counts().plot(kind="bar")
plt.title("Medicamentos Mais Coletados")
>>>>>>> b8623c99592493d5c84f74dfda2d58e9cf026c58
plt.xlabel("Medicamento")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_medicamentos.png")
plt.close()


<<<<<<< HEAD
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
=======
print("\nLocalizações mais consultadas:")
print(df["localizacao"].value_counts())

plt.figure(figsize=(8, 5))
df["localizacao"].value_counts().plot(kind="bar")
plt.title("Localizações Mais Consultadas")
plt.xlabel("Localização")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_localizacao.png")
plt.close()


print("\nCategoria de preço:")
print(df["categoria_preco"].value_counts())

plt.figure(figsize=(8, 5))
df["categoria_preco"].value_counts().plot(kind="bar")
plt.title("Distribuição das Categorias de Preço")
plt.xlabel("Categoria")
>>>>>>> b8623c99592493d5c84f74dfda2d58e9cf026c58
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_categoria_preco.png")
plt.close()


<<<<<<< HEAD
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
=======
df.to_csv("dataset_medicamentos_limpo.csv", index=False, encoding="utf-8-sig")

print("\nDataset limpo salvo como dataset_medicamentos_limpo.csv")
print("Gráficos gerados com sucesso.")
>>>>>>> b8623c99592493d5c84f74dfda2d58e9cf026c58
