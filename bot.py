from botcity.web import WebBot, Browser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

import pandas as pd
import time
import re
import os
import requests
from urllib.parse import quote_plus


load_dotenv()


def enviar_telegram(mensagem):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Token ou Chat ID não encontrado no .env")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    dados = {
        "chat_id": chat_id,
        "text": mensagem
    }

    for tentativa in range(3):
        try:
            resposta = requests.post(
                url,
                data=dados,
                timeout=20
            )

            print("Telegram:", resposta.status_code)
            print(resposta.text)

            if resposta.status_code == 200:
                return

        except Exception as erro:
            print(f"Erro ao enviar Telegram na tentativa {tentativa + 1}:", erro)
            time.sleep(3)

    print("Não foi possível enviar mensagem no Telegram.")


def extrair_preco(texto):
    precos = re.findall(r"R\$\s?\d+[\.,]\d{2}", texto)

    if precos:
        return precos[-1]

    return "Preço não encontrado"


def preco_para_float(preco_texto):
    try:
        preco_limpo = (
            preco_texto
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )

        return float(preco_limpo)

    except:
        return None


def coletar_produtos(
    bot,
    farmacia,
    url_busca,
    medicamento,
    preco_maximo,
    localizacao,
    limite=5
):
    resultados = []
    busca = quote_plus(medicamento)
    url = url_busca + busca

    print(f"\nPesquisando {medicamento} na {farmacia}...")

    bot.browse(url)
    time.sleep(8)

    links = bot.driver.find_elements(By.TAG_NAME, "a")

    encontrados = 0

    for item in links:
        if encontrados >= limite:
            break

        try:
            titulo = item.text.strip()
            link = item.get_attribute("href")

            if (
                titulo
                and link
                and medicamento.lower() in titulo.lower()
            ):
                texto_card = item.find_element(By.XPATH, "..").text

                preco = extrair_preco(texto_card)
                preco_numero = preco_para_float(preco)

                if preco_numero is not None and preco_numero <= float(preco_maximo):
                    alerta = "SIM"
                else:
                    alerta = "NÃO"

                print("FARMÁCIA:", farmacia)
                print("PRODUTO:", titulo)
                print("PREÇO:", preco)
                print("ALERTA:", alerta)
                print("LINK:", link)

                resultados.append({
                    "medicamento": medicamento,
                    "preco_maximo": preco_maximo,
                    "localizacao": localizacao,
                    "farmacia": farmacia,
                    "titulo": titulo,
                    "preco": preco,
                    "preco_numero": preco_numero,
                    "alerta": alerta,
                    "link": link
                })

                encontrados += 1

        except Exception:
            pass

    return resultados


def montar_resumo_telegram(df):
    if df.empty:
        return "💊 MediAlert AM\n\nNenhum medicamento foi encontrado na busca."

    mensagem = "💊 MediAlert AM - Resultado da busca\n\n"

    for medicamento in df["medicamento"].unique():
        dados_med = df[df["medicamento"] == medicamento]

        mensagem += f"🔎 {medicamento}\n"

        for _, linha in dados_med.head(3).iterrows():
            mensagem += (
                f"- {linha['farmacia']}: {linha['titulo']}\n"
                f"  Preço: {linha['preco']}\n"
                f"  Link: {linha['link']}\n"
            )

        mensagem += "\n"

    if len(mensagem) > 3500:
        mensagem = mensagem[:3500] + "\n\nMensagem cortada para caber no Telegram."

    return mensagem


def main():
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

    medicamentos = pd.read_csv("medicamentos.csv")

    farmacias = [
        {
            "nome": "Drogasil",
            "url": "https://www.drogasil.com.br/search?w="
        },
        {
            "nome": "Bemol Farma",
            "url": "https://www.bemolfarma.com.br/busca?q="
        },
        {
            "nome": "Pague Menos",
            "url": "https://www.paguemenos.com.br/busca/"
        },
        {
            "nome": "FarmaBem",
            "url": "https://farmabem.com.br/busca?q="
        }
    ]

    todos_resultados = []

    for _, item in medicamentos.iterrows():
        medicamento = item["medicamento"]
        preco_maximo = item["preco_maximo"]
        localizacao = item["localizacao"]

        for farmacia in farmacias:
            try:
                resultados = coletar_produtos(
                    bot=bot,
                    farmacia=farmacia["nome"],
                    url_busca=farmacia["url"],
                    medicamento=medicamento,
                    preco_maximo=preco_maximo,
                    localizacao=localizacao,
                    limite=5
                )

                todos_resultados.extend(resultados)

            except Exception as erro:
                print(f"Erro na farmácia {farmacia['nome']}:", erro)

    df = pd.DataFrame(todos_resultados)

    if not df.empty:
        df = df.drop_duplicates(
            subset=["medicamento", "farmacia", "titulo", "link"]
        )

    df.to_csv(
        "resultados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nCSV salvo com sucesso!")

    mensagem = montar_resumo_telegram(df)
    enviar_telegram(mensagem)

    bot.stop_browser()


if __name__ == "__main__":
    main()