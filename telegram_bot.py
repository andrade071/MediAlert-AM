import os
import time
import re
import requests
import pandas as pd

from dotenv import load_dotenv
from urllib.parse import quote_plus

from botcity.web import WebBot, Browser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


load_dotenv()


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_mensagem(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    dados = {
        "chat_id": chat_id,
        "text": texto
    }

    requests.post(url, data=dados, timeout=20)


def buscar_medicamento(medicamento, localizacao):
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

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

    resultados = []

    for farmacia in farmacias:
        try:
            busca = quote_plus(medicamento)
            url = farmacia["url"] + busca

            print(f"Pesquisando {medicamento} na {farmacia['nome']}...")

            bot.browse(url)
            time.sleep(7)

            links = bot.driver.find_elements(By.TAG_NAME, "a")

            encontrados = 0

            for item in links:
                if encontrados >= 3:
                    break

                titulo = item.text.strip()
                link = item.get_attribute("href")

                if (
                    titulo
                    and link
                    and medicamento.lower() in titulo.lower()
                ):
                    resultados.append({
                        "farmacia": farmacia["nome"],
                        "titulo": titulo,
                        "link": link
                    })

                    encontrados += 1

        except Exception as erro:
            print(f"Erro na {farmacia['nome']}: {erro}")

    bot.stop_browser()

    return resultados


def montar_resposta(medicamento, localizacao, resultados):
    if not resultados:
        return (
            f"💊 MediAlert AM\n\n"
            f"Não encontrei resultados para: {medicamento}\n"
            f"📍 Local informado: {localizacao}"
        )

    resposta = (
        f"💊 MediAlert AM\n\n"
        f"Medicamento: {medicamento}\n"
        f"📍 Local informado: {localizacao}\n\n"
    )

    for item in resultados[:8]:
        resposta += (
            f"🏥 {item['farmacia']}\n"
            f"{item['titulo']}\n"
            f"{item['link']}\n\n"
        )

    if len(resposta) > 3500:
        resposta = resposta[:3500] + "\n\nMensagem reduzida para caber no Telegram."

    return resposta


def ler_mensagens(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    params = {
        "timeout": 30,
        "offset": offset
    }

    resposta = requests.get(url, params=params, timeout=40)
    return resposta.json()


def main():
    print("MediAlert AM Telegram iniciado...")
    print("Envie no Telegram: medicamento | localização")
    print("Exemplo: dipirona | Adrianópolis Manaus")

    offset = None

    while True:
        try:
            dados = ler_mensagens(offset)

            for update in dados.get("result", []):
                offset = update["update_id"] + 1

                mensagem = update.get("message", {})
                texto = mensagem.get("text", "")
                chat_id = mensagem.get("chat", {}).get("id")

                if not texto or not chat_id:
                    continue

                if "|" not in texto:
                    enviar_mensagem(
                        chat_id,
                        "Envie no formato:\nmedicamento | localização\n\nExemplo:\ndipirona | Adrianópolis Manaus"
                    )
                    continue

                medicamento, localizacao = texto.split("|", 1)

                medicamento = medicamento.strip()
                localizacao = localizacao.strip()

                enviar_mensagem(
                    chat_id,
                    f"🔎 Buscando {medicamento} próximo de {localizacao}..."
                )

                resultados = buscar_medicamento(medicamento, localizacao)

                resposta = montar_resposta(
                    medicamento,
                    localizacao,
                    resultados
                )

                enviar_mensagem(chat_id, resposta)

        except Exception as erro:
            print("Erro geral:", erro)
            time.sleep(5)


if __name__ == "__main__":
    main()