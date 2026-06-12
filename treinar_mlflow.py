import os
import pandas as pd
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay
)


df = pd.read_csv("dataset_medicamentos_limpo.csv")

df["relevante"] = df["relevante"].fillna(0).astype(int)

X = df[
    [
        "medicamento",
        "farmacia",
        "localizacao",
        "categoria_preco"
    ]
]

y = df["relevante"]

cat_features = [
    "medicamento",
    "farmacia",
    "localizacao",
    "categoria_preco"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore"))
                ]
            ),
            cat_features
        )
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

modelos = {
    "LogisticRegression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),

    "RandomForest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    ),

    "GradientBoosting": GradientBoostingClassifier(
        random_state=42
    )
}

mlflow.set_experiment("MediAlert_AM")

os.makedirs("img", exist_ok=True)

melhor_modelo_nome = None
melhor_pipeline = None
melhor_f1 = -1
melhores_preds = None

resultados = []

for nome, modelo in modelos.items():

    with mlflow.start_run(run_name=nome):

        pipeline = Pipeline(
            [
                ("prep", preprocessor),
                ("modelo", modelo)
            ]
        )

        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)

        acc = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds, zero_division=0)
        recall = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(pipeline, nome)

        resultados.append({
            "modelo": nome,
            "accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        })

        print("=" * 60)
        print(nome)
        print(f"Accuracy : {acc:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1-score : {f1:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, preds, zero_division=0))

        if f1 > melhor_f1:
            melhor_f1 = f1
            melhor_modelo_nome = nome
            melhor_pipeline = pipeline
            melhores_preds = preds


df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(
    "resultados_modelos.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nResultados salvos em resultados_modelos.csv")
print("\nMelhor modelo pelo F1-score:", melhor_modelo_nome)


# ==========================
# MATRIZ DE CONFUSÃO
# ==========================

fig, ax = plt.subplots(figsize=(7, 5))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    melhores_preds,
    display_labels=["Não relevante", "Relevante"],
    cmap="Reds",
    ax=ax
)

plt.title(f"Matriz de Confusão - {melhor_modelo_nome}")
plt.tight_layout()

plt.savefig("matriz_confusao.png", dpi=300, bbox_inches="tight")
plt.savefig("img/matriz_confusao.png", dpi=300, bbox_inches="tight")
plt.close()


# ==========================
# GRÁFICO DOS MODELOS
# ==========================

df_plot = df_resultados.set_index("modelo")

plt.figure(figsize=(8, 5))
df_plot["accuracy"].plot(kind="bar")

plt.title("Comparativo de Accuracy dos Modelos")
plt.xlabel("Modelo")
plt.ylabel("Accuracy")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()

plt.savefig("grafico_modelos.png", dpi=300, bbox_inches="tight")
plt.savefig("img/grafico_modelos.png", dpi=300, bbox_inches="tight")
plt.close()

print("matriz_confusao.png gerada com sucesso.")
print("grafico_modelos.png atualizado com sucesso.")   