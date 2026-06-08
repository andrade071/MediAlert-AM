import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import accuracy_score


df = pd.read_csv("dataset_medicamentos_limpo.csv")

df["relevante"] = df["relevante"].fillna(0)

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
                    (
                        "imputer",
                        SimpleImputer(strategy="most_frequent")
                    ),
                    (
                        "encoder",
                        OneHotEncoder(handle_unknown="ignore")
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

mlflow.set_experiment(
    "MediAlert_AM"
)

for nome, modelo in modelos.items():

    with mlflow.start_run(run_name=nome):

        pipeline = Pipeline(
            [
                ("prep", preprocessor),
                ("modelo", modelo)
            ]
        )

        pipeline.fit(
            X_train,
            y_train
        )

        preds = pipeline.predict(
            X_test
        )

        acc = accuracy_score(
            y_test,
            preds
        )

        mlflow.log_metric(
            "accuracy",
            acc
        )

        mlflow.sklearn.log_model(
            pipeline,
            nome
        )

        print(
            f"{nome} -> Accuracy = {acc}"
        )