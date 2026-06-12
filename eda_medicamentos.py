import pandas as pd
import matplotlib.pyplot as plt
import os


# ==========================
# CONFIGURAÇÕES
# ==========================

ARQUIVO_ENTRADA = "dataset_medicamentos.csv"
ARQUIVO_SAIDA = "dataset_medicamentos_limpo.csv"

PASTA_IMG = "img"
os.makedirs(PASTA_IMG, exist_ok=True)


# ==========================
# CARREGAR DATASET
# ==========================

df = pd.read_csv(ARQUIVO_ENTRADA)

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

colunas_texto = [
    "medicamento",
    "localizacao",
    "farmacia",
    "titulo",
    "categoria_preco"
]

for coluna in colunas_texto:
    if coluna in df.columns:
        df[coluna] = df[coluna].astype(str).str.lower().str.strip()

if "preco_numero" in df.columns:
    df["preco_numero"] = pd.to_numeric(df["preco_numero"], errors="coerce")

if "relevante" in df.columns:
    df["relevante"] = df["relevante"].fillna(0).astype(int)

linhas_antes = len(df)

colunas_duplicadas = [
    "medicamento",
    "localizacao",
    "farmacia",
    "titulo",
    "link"
]

colunas_existentes = [
    coluna for coluna in colunas_duplicadas if coluna in df.columns
]

if colunas_existentes:
    df = df.drop_duplicates(subset=colunas_existentes)
else:
    df = df.drop_duplicates()

linhas_depois = len(df)

print(f"\nLinhas antes da limpeza: {linhas_antes}")
print(f"Linhas depois da limpeza: {linhas_depois}")
print(f"Linhas removidas: {linhas_antes - linhas_depois}")


# ==========================
# EDA
# ==========================

print("\n" + "=" * 60)
print("EDA - ANÁLISE EXPLORATÓRIA")
print("=" * 60)

print("\nProdutos por farmácia:")
if "farmacia" in df.columns:
    print(df["farmacia"].value_counts())

print("\nTop 10 medicamentos mais coletados:")
if "medicamento" in df.columns:
    print(df["medicamento"].value_counts().head(10))

print("\nTop 10 localizações mais consultadas:")
if "localizacao" in df.columns:
    print(df["localizacao"].value_counts().head(10))

print("\nCategoria de preço:")
if "categoria_preco" in df.columns:
    print(df["categoria_preco"].value_counts())

if "relevante" in df.columns:
    print("\nDistribuição da variável alvo relevante:")
    print(df["relevante"].value_counts())


# ==========================
# GRÁFICO 1 - FARMÁCIAS
# ==========================

if "farmacia" in df.columns:
    plt.figure(figsize=(10, 6))
    df["farmacia"].value_counts().plot(kind="bar")
    plt.title("Distribuição de Registros por Farmácia")
    plt.xlabel("Farmácia")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("grafico_farmacias.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{PASTA_IMG}/grafico_farmacias.png", dpi=300, bbox_inches="tight")
    plt.close()


# ==========================
# GRÁFICO 2 - MEDICAMENTOS
# ==========================

if "medicamento" in df.columns:
    plt.figure(figsize=(10, 6))
    df["medicamento"].value_counts().head(10).plot(kind="bar")
    plt.title("Top 10 Medicamentos Mais Coletados")
    plt.xlabel("Medicamento")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("grafico_medicamentos.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{PASTA_IMG}/grafico_medicamentos.png", dpi=300, bbox_inches="tight")
    plt.close()


# ==========================
# GRÁFICO 3 - LOCALIZAÇÕES
# ==========================

if "localizacao" in df.columns:
    plt.figure(figsize=(10, 6))
    df["localizacao"].value_counts().head(10).plot(kind="barh")
    plt.title("Top 10 Localizações Consultadas")
    plt.xlabel("Quantidade")
    plt.ylabel("Localização")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("grafico_localizacoes.png", dpi=300, bbox_inches="tight")
    plt.savefig("grafico_localizacao.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{PASTA_IMG}/grafico_localizacoes.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{PASTA_IMG}/grafico_localizacao.png", dpi=300, bbox_inches="tight")
    plt.close()


# ==========================
# GRÁFICO 4 - CATEGORIA DE PREÇO
# ==========================

if "categoria_preco" in df.columns:
    plt.figure(figsize=(8, 6))
    df["categoria_preco"].value_counts().plot(kind="bar")
    plt.title("Distribuição por Categoria de Preço")
    plt.xlabel("Categoria de Preço")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("grafico_categoria_preco.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{PASTA_IMG}/grafico_categoria_preco.png", dpi=300, bbox_inches="tight")
    plt.close()

# ==========================
# GRÁFICO 5 - RELEVÂNCIA
# ==========================

if "relevante" in df.columns:
    contagem_relevancia = df["relevante"].value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    ax = contagem_relevancia.plot(kind="bar")

    plt.title("Distribuição da Classe Alvo")
    plt.xlabel("Classe")
    plt.ylabel("Quantidade")

    labels = []
    for valor in contagem_relevancia.index:
        if valor == 0:
            labels.append("0 - Não relevante")
        else:
            labels.append("1 - Relevante")

    plt.xticks(
        ticks=range(len(contagem_relevancia.index)),
        labels=labels,
        rotation=0
    )

    for i, valor in enumerate(contagem_relevancia.values):
        ax.text(
            i,
            valor + 20,
            str(valor),
            ha="center",
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig("grafico_relevancia.png", dpi=300, bbox_inches="tight")
    plt.savefig("grafico_classe_alvo.png", dpi=300, bbox_inches="tight")
    plt.savefig("img/grafico_relevancia.png", dpi=300, bbox_inches="tight")
    plt.savefig("img/grafico_classe_alvo.png", dpi=300, bbox_inches="tight")
    plt.close()
    
# ==========================
# GRÁFICO 6 - HISTOGRAMA DE PREÇOS
# ==========================

if "preco_numero" in df.columns:
    df_precos = df.dropna(subset=["preco_numero"])

    if len(df_precos) > 0:
        plt.figure(figsize=(10, 6))
        df_precos["preco_numero"].hist(bins=25)
        plt.title("Distribuição dos Preços Coletados")
        plt.xlabel("Preço (R$)")
        plt.ylabel("Frequência")
        plt.tight_layout()
        plt.savefig("grafico_histograma_precos.png", dpi=300, bbox_inches="tight")
        plt.savefig("grafico_precos.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{PASTA_IMG}/grafico_histograma_precos.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"{PASTA_IMG}/grafico_precos.png", dpi=300, bbox_inches="tight")
        plt.close()


# ==========================
# SALVAR DATASET LIMPO
# ==========================

df.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 60)
print("ARQUIVOS GERADOS")
print("=" * 60)

print(ARQUIVO_SAIDA)
print("grafico_farmacias.png")
print("grafico_medicamentos.png")
print("grafico_localizacoes.png")
print("grafico_categoria_preco.png")
print("grafico_relevancia.png")
print("grafico_classe_alvo.png")
print("grafico_histograma_precos.png")
print("grafico_precos.png")

print("\nTambém foram salvos na pasta img/ para usar nos slides.")

print("\nEDA finalizada com sucesso!")