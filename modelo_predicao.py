import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


print("=" * 50)
print("CARREGANDO DATASET")
print("=" * 50)

df = pd.read_csv("dataset_medicamentos_limpo.csv")

# corrigir nulos

df["relevante"] = df["relevante"].fillna(0)

df["preco_numero"] = df["preco_numero"].fillna(
    df["preco_numero"].median()
)

print(df.shape)

# variáveis

X = df[
    [
        "medicamento",
        "farmacia",
        "localizacao",
        "categoria_preco"
    ]
]

y = df["relevante"]

# pré-processamento

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
                steps=[
                    (
                        "imputer",
                        SimpleImputer(strategy="most_frequent")
                    ),
                    (
                        "encoder",
                        OneHotEncoder(
                            handle_unknown="ignore"
                        )
                    )
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
    random_state=42
)

modelos = {
    "LogisticRegression":
        LogisticRegression(max_iter=1000),

    "RandomForest":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ),

    "GradientBoosting":
        GradientBoostingClassifier(
            random_state=42
        )
}

for nome, modelo in modelos.items():

    print("\n")
    print("=" * 50)
    print(nome)
    print("=" * 50)

    pipeline = Pipeline(
        steps=[
            ("preprocessamento", preprocessor),
            ("modelo", modelo)
        ]
    )

    pipeline.fit(X_train, y_train)

    previsoes = pipeline.predict(X_test)

    acc = accuracy_score(
        y_test,
        previsoes
    )

    print("Accuracy:", acc)

    print(
        classification_report(
            y_test,
            previsoes
        )
    )