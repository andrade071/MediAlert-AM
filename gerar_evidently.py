import pandas as pd
from evidently import Report
from evidently.presets import DataSummaryPreset


df = pd.read_csv("dataset_medicamentos_limpo.csv")

report = Report([
    DataSummaryPreset()
])

snapshot = report.run(df, None)

snapshot.save_html("evidently_report.html")

print("Relatório Evidently gerado: evidently_report.html")