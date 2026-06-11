from bot import coletar_produtos, salvar_dataset, criar_bot, FARMACIAS
import pandas as pd
import time
import os


MEDICAMENTOS = [
    "dipirona",
    "paracetamol",
    "ibuprofeno",
    "loratadina",
    "omeprazol",
    "losartana",
    "amitriptilina",
    "dorflex",
    "neosaldina",
    "vitamina c",
    "nimesulida",
    "cetirizina",
    "amoxicilina",
    "simeticona",
    "buscopan"
]

BAIRROS = [
    "Centro Manaus",
    "Adrianópolis Manaus",
    "Zumbi Manaus",
    "Jorge Teixeira Manaus",
    "Santo Agostinho Manaus",
    "Parque 10 Manaus",
    "Cidade Nova Manaus",
    "Compensa Manaus",
    "Flores Manaus",
    "Tarumã Manaus"
]

PRECOS_MAXIMOS = {
    "dipirona": 30,
    "paracetamol": 30,
    "ibuprofeno": 40,
    "loratadina": 35,
    "omeprazol": 50,
    "losartana": 50,
    "amitriptilina": 80,
    "dorflex": 35,
    "neosaldina": 35,
    "vitamina c": 40,
    "nimesulida": 35,
    "cetirizina": 35,
    "amoxicilina": 60,
    "simeticona": 35,
    "buscopan": 45
}


def gerar_combinacoes():
    combinacoes = []

    for medicamento in MEDICAMENTOS:
        for bairro in BAIRROS:
            combinacoes.append({
                "medicamento": medicamento,
                "preco_maximo": PRECOS_MAXIMOS.get(medicamento, 50),
                "localizacao": bairro
            })

    return combinacoes


def main():
    print("=" * 70)
    print("COLETA AUTOMÁTICA - MEDIALERT AM")
    print("=" * 70)

    combinacoes = gerar_combinacoes()
    todos_resultados = []

    bot = criar_bot()

    try:
        total = len(combinacoes)

        for indice, item in enumerate(combinacoes, start=1):
            medicamento = item["medicamento"]
            preco_maximo = item["preco_maximo"]
            localizacao = item["localizacao"]

            print("\n" + "=" * 70)
            print(f"Coleta {indice}/{total}")
            print(f"Medicamento: {medicamento}")
            print(f"Localização: {localizacao}")
            print("=" * 70)

            for farmacia in FARMACIAS:
                resultados = coletar_produtos(
                    bot=bot,
                    farmacia=farmacia["nome"],
                    url_busca=farmacia["url"],
                    medicamento=medicamento,
                    preco_maximo=preco_maximo,
                    localizacao=localizacao,
                    limite=15
                )

                todos_resultados.extend(resultados)

                salvar_dataset(todos_resultados)

                time.sleep(3)

    finally:
        try:
            bot.stop_browser()
        except Exception:
            pass

    df = pd.DataFrame(todos_resultados)

    df.to_csv(
        "resultados_coleta_automatica.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n" + "=" * 70)
    print("COLETA FINALIZADA")
    print("=" * 70)
    print(f"Total coletado nesta execução: {len(df)}")
    print("Arquivo salvo: resultados_coleta_automatica.csv")
    print("Dataset atualizado: dataset_medicamentos.csv")


if __name__ == "__main__":
    main()