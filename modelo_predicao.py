import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


df = pd.read_csv("dataset_medicamentos_limpo.csv")

print("=" * 50)
print("CRISP-DM - MODELING")
print("=" * 50)

df_modelo = df[df["categoria_preco"] != "indefinido"].copy()

if df_modelo.empty:
    print("Não há preços suficientes para treinar o modelo.")
    print("Como alternativa, será criada uma predição baseada na farmácia e medicamento para categoria simulada.")

    df_modelo = df.copy()

    def categoria_simulada(row):
        texto = row["titulo"].lower()

        if "genérico" in texto or "generico" in texto:
            return "baixo"
        if "tylenol" in texto or "novalgina" in texto or "claritin" in texto:
            return "alto"
        return "medio"

    df_modelo["categoria_preco"] = df_modelo.apply(categoria_simulada, axis=1)


colunas_entrada = ["medicamento", "farmacia", "localizacao", "titulo"]
alvo = "categoria_preco"

X = df_modelo[colunas_entrada]
y = df_modelo[alvo]

preprocessador = ColumnTransformer(
    transformers=[
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), colunas_entrada)
    ]
)

modelo = Pipeline(
    steps=[
        ("preprocessador", preprocessador),
        ("classificador", DecisionTreeClassifier(random_state=42))
    ]
)

if len(df_modelo) < 10:
    print("Dataset pequeno. O modelo será treinado com todos os dados apenas para demonstração.")
    modelo.fit(X, y)
    y_pred = modelo.predict(X)

    print("\nAcurácia demonstrativa:")
    print(accuracy_score(y, y_pred))

else:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42
    )

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    print("\nAcurácia:")
    print(accuracy_score(y_test, y_pred))

    print("\nRelatório de classificação:")
    print(classification_report(y_test, y_pred))

    print("\nMatriz de confusão:")
    print(confusion_matrix(y_test, y_pred))


print("\n" + "=" * 50)
print("PREDIÇÃO DE EXEMPLO")
print("=" * 50)

novo_dado = pd.DataFrame([{
    "medicamento": "dipirona",
    "farmacia": "Drogasil",
    "localizacao": "Centro Manaus",
    "titulo": "Dipirona Monoidratada Genérico 500mg"
}])

predicao = modelo.predict(novo_dado)

print("Entrada:")
print(novo_dado)

print("\nCategoria prevista:")
print(predicao[0])