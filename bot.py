from botcity.web import WebBot, Browser
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

import pandas as pd
import time
import re
import os
import requests
from datetime import datetime
from urllib.parse import quote_plus


load_dotenv()

ARQUIVO_ENTRADA = "medicamentos.csv"
ARQUIVO_SAIDA = "dataset_medicamentos.csv"
LIMITE_POR_FARMACIA = 15

CHROMEDRIVER_PATH = r"C:\chromedriver\chromedriver.exe"

FARMACIAS = [
    {
        "nome": "Drogasil",
        "url": "https://www.drogasil.com.br/search?w={busca}"
    },
    {
        "nome": "Droga Raia",
        "url": "https://www.drogaraia.com.br/search?w={busca}"
    },
    {
        "nome": "Ultrafarma",
        "url": "https://www.ultrafarma.com.br/busca?q={busca}"
    }
]


def enviar_telegram(mensagem):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Token ou Chat ID não encontrado no .env")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        resposta = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": mensagem
            },
            timeout=20
        )
        print("Telegram:", resposta.status_code)

    except Exception as erro:
        print("Erro ao enviar Telegram:", erro)


def extrair_preco(texto):
    if not texto:
        return "Preço não encontrado"

    precos = re.findall(r"R\$\s?\d+[\.,]\d{2}", texto)

    if precos:
        return precos[-1]

    return "Preço não encontrado"


def preco_para_float(preco_texto):
    try:
        return float(
            preco_texto
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )
    except Exception:
        return None


def classificar_preco(preco_numero):
    if preco_numero is None:
        return "indefinido"

    if preco_numero <= 20:
        return "baixo"

    if preco_numero <= 50:
        return "medio"

    return "alto"


def definir_alerta(preco_numero, preco_maximo):
    try:
        if preco_numero is not None and preco_numero <= float(preco_maximo):
            return "SIM"
        return "NÃO"
    except Exception:
        return "NÃO"


def definir_relevancia(medicamento, titulo, preco_numero, preco_maximo):
    medicamento = str(medicamento).lower()
    titulo = str(titulo).lower()

    if medicamento not in titulo:
        return 0

    if preco_numero is None:
        return 1

    try:
        if preco_numero <= float(preco_maximo):
            return 1
        return 0
    except Exception:
        return 1


def criar_bot():
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME

    bot.driver_path = r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    return bot


def coletar_produtos(
    bot,
    farmacia,
    url_busca,
    medicamento,
    preco_maximo,
    localizacao,
    limite=15
):
    resultados = []

    busca = quote_plus(str(medicamento))
    url = url_busca.format(busca=busca)

    print("=" * 70)
    print(f"Pesquisando {medicamento} na {farmacia}")
    print(url)
    print("=" * 70)

    try:
        bot.browse(url)
        time.sleep(8)

        try:
            texto_pagina = bot.driver.find_element(By.TAG_NAME, "body").text
            linhas = texto_pagina.split("\n")
        except Exception:
            linhas = []

        links = bot.driver.find_elements(By.TAG_NAME, "a")

        encontrados = 0

        for item in links:
            if encontrados >= limite:
                break

            try:
                titulo = item.text.strip()
                link = item.get_attribute("href")

                if not titulo or not link:
                    continue

                if "http" not in link:
                    continue

                if str(medicamento).lower() not in titulo.lower():
                    continue

                preco = "Preço não encontrado"

                for i, linha in enumerate(linhas):
                    if titulo.lower() in linha.lower():
                        trecho = "\n".join(linhas[i:i + 12])
                        preco = extrair_preco(trecho)
                        break

                if preco == "Preço não encontrado":
                    try:
                        texto_card = item.find_element(By.XPATH, "..").text
                        preco = extrair_preco(texto_card)
                    except Exception:
                        pass

                preco_numero = preco_para_float(preco)
                categoria_preco = classificar_preco(preco_numero)
                alerta = definir_alerta(preco_numero, preco_maximo)

                relevante = definir_relevancia(
                    medicamento,
                    titulo,
                    preco_numero,
                    preco_maximo
                )

                resultado = {
                    "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "medicamento": str(medicamento).lower(),
                    "preco_maximo": preco_maximo,
                    "localizacao": localizacao,
                    "farmacia": farmacia,
                    "titulo": titulo,
                    "preco": preco,
                    "preco_numero": preco_numero,
                    "categoria_preco": categoria_preco,
                    "alerta": alerta,
                    "relevante": relevante,
                    "link": link
                }

                resultados.append(resultado)

                print("FARMÁCIA:", farmacia)
                print("PRODUTO:", titulo)
                print("PREÇO:", preco)
                print("CATEGORIA:", categoria_preco)
                print("ALERTA:", alerta)
                print("RELEVANTE:", relevante)
                print("LINK:", link)
                print("-" * 60)

                encontrados += 1

            except Exception:
                pass

        print(f"{farmacia}: {len(resultados)} resultados coletados.")

    except Exception as erro:
        print(f"Erro na farmácia {farmacia}:", erro)

    return resultados


def salvar_dataset(resultados):
    if not resultados:
        print("Nenhum resultado para salvar.")
        return

    df_novo = pd.DataFrame(resultados)

    try:
        df_antigo = pd.read_csv(ARQUIVO_SAIDA)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
    except FileNotFoundError:
        df_final = df_novo

    df_final = df_final.drop_duplicates(
        subset=[
            "medicamento",
            "localizacao",
            "farmacia",
            "titulo",
            "link"
        ]
    )

    df_final.to_csv(
        ARQUIVO_SAIDA,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDataset salvo com sucesso!")
    print("Arquivo:", ARQUIVO_SAIDA)
    print("Linhas e colunas:", df_final.shape)


def montar_resumo_telegram(df):
    if df.empty:
        return "💊 MediAlert AM\n\nNenhum medicamento foi encontrado na busca."

    mensagem = "💊 MediAlert AM - Resultado da coleta\n\n"
    mensagem += f"Total coletado nesta execução: {len(df)} registros\n\n"

    for medicamento in df["medicamento"].unique():
        dados_med = df[df["medicamento"] == medicamento]

        mensagem += f"🔎 {medicamento}\n"

        for _, linha in dados_med.head(3).iterrows():
            mensagem += (
                f"- {linha['farmacia']}: {linha['titulo']}\n"
                f"  Preço: {linha['preco']}\n"
                f"  Categoria: {linha['categoria_preco']}\n"
                f"  Relevante: {linha['relevante']}\n"
                f"  Link: {linha['link']}\n"
            )

        mensagem += "\n"

    if len(mensagem) > 3500:
        mensagem = mensagem[:3500] + "\n\nMensagem cortada para caber no Telegram."

    return mensagem


def main():
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"Arquivo {ARQUIVO_ENTRADA} não encontrado.")
        print("Crie um arquivo medicamentos.csv com as colunas:")
        print("medicamento,preco_maximo,localizacao")
        return

    medicamentos = pd.read_csv(ARQUIVO_ENTRADA)

    colunas_necessarias = [
        "medicamento",
        "preco_maximo",
        "localizacao"
    ]

    for coluna in colunas_necessarias:
        if coluna not in medicamentos.columns:
            print(f"Coluna obrigatória ausente no CSV: {coluna}")
            return

    bot = criar_bot()
    todos_resultados = []

    try:
        for _, item in medicamentos.iterrows():
            medicamento = item["medicamento"]
            preco_maximo = item["preco_maximo"]
            localizacao = item["localizacao"]

            for farmacia in FARMACIAS:
                resultados = coletar_produtos(
                    bot=bot,
                    farmacia=farmacia["nome"],
                    url_busca=farmacia["url"],
                    medicamento=medicamento,
                    preco_maximo=preco_maximo,
                    localizacao=localizacao,
                    limite=LIMITE_POR_FARMACIA
                )

                todos_resultados.extend(resultados)
                time.sleep(3)

    finally:
        try:
            bot.stop_browser()
        except Exception:
            pass

    salvar_dataset(todos_resultados)

    df_execucao = pd.DataFrame(todos_resultados)

    df_execucao.to_csv(
        "resultados_execucao.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nCSV da execução salvo como resultados_execucao.csv")

    mensagem = montar_resumo_telegram(df_execucao)
    enviar_telegram(mensagem)


if __name__ == "__main__":
    main()