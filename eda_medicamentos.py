import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("dataset_medicamentos.csv")

print("=" * 50)
print("CRISP-DM - DATA UNDERSTANDING")
print("=" * 50)

print("\nDimensão do dataset:")
print(df.shape)

print("\nPrimeiras linhas:")
print(df.head())

print("\nTipos de dados:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

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

print("\nProdutos por farmácia:")
print(df["farmacia"].value_counts())

plt.figure(figsize=(8, 5))
df["farmacia"].value_counts().plot(kind="bar")
plt.title("Quantidade de Produtos por Farmácia")
plt.xlabel("Farmácia")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_farmacias.png")
plt.close()


print("\nMedicamentos mais coletados:")
print(df["medicamento"].value_counts())

plt.figure(figsize=(8, 5))
df["medicamento"].value_counts().plot(kind="bar")
plt.title("Medicamentos Mais Coletados")
plt.xlabel("Medicamento")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_medicamentos.png")
plt.close()


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
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig("grafico_categoria_preco.png")
plt.close()


df.to_csv("dataset_medicamentos_limpo.csv", index=False, encoding="utf-8-sig")

print("\nDataset limpo salvo como dataset_medicamentos_limpo.csv")
print("Gráficos gerados com sucesso.")