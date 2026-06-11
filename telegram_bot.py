import os
import time
import re
import requests
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import quote_plus

from botcity.web import WebBot, Browser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


FARMACIAS = [
    {
        "nome": "Drogasil",
        "url": "https://www.drogasil.com.br/search?w={busca}"
    },
    {
        "nome": "Drogaria São Paulo",
        "url": "https://www.drogariasaopaulo.com.br/medicamentos/com%20{busca}"
    },
    {
        "nome": "Pague Menos",
        "url": "https://www.paguemenos.com.br/medicamentos-e-saude?terms={busca}"
    },
    {
        "nome": "Droga Raia",
        "url": "https://www.drogaraia.com.br/search?w={busca}"
    }
]


def enviar_mensagem(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    dados = {
        "chat_id": chat_id,
        "text": texto
    }

    try:
        requests.post(url, data=dados, timeout=20)
    except Exception as erro:
        print("Erro ao enviar mensagem:", erro)


def extrair_preco(texto):
    precos = re.findall(r"R\$\s?\d+[\.,]\d{2}", texto)

    if precos:
        return precos[-1]

    return "Preço não encontrado"


def preco_para_float(preco):
    try:
        return float(
            preco.replace("R$", "")
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


def definir_relevancia(medicamento, titulo, preco_numero):
    medicamento = medicamento.lower()
    titulo = titulo.lower()

    if medicamento not in titulo:
        return 0

    if preco_numero is not None:
        if preco_numero <= 30:
            return 1
        return 0

    return 1


def salvar_resultados(resultados):
    if not resultados:
        print("Nenhum resultado novo para salvar.")
        return

    arquivo = "dataset_medicamentos.csv"

    df_novo = pd.DataFrame(resultados)

    try:
        df_antigo = pd.read_csv(arquivo)
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
        arquivo,
        index=False,
        encoding="utf-8-sig"
    )

    print("Dataset salvo com sucesso!")
    print("Total atual:", df_final.shape)


def coletar_links_pagina(bot, medicamento, localizacao, farmacia_nome, limite=10):
    resultados = []
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        texto_pagina = bot.driver.find_element(By.TAG_NAME, "body").text
        linhas = texto_pagina.split("\n")
    except Exception:
        texto_pagina = ""
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

            if medicamento.lower() not in titulo.lower():
                continue

            if "http" not in link:
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

            relevante = definir_relevancia(
                medicamento,
                titulo,
                preco_numero
            )

            resultado = {
                "data_hora": data_hora,
                "medicamento": medicamento.lower(),
                "localizacao": localizacao,
                "farmacia": farmacia_nome,
                "titulo": titulo,
                "preco": preco,
                "preco_numero": preco_numero,
                "categoria_preco": categoria_preco,
                "link": link,
                "relevante": relevante
            }

            resultados.append(resultado)

            print("-" * 60)
            print("FARMÁCIA:", farmacia_nome)
            print("PRODUTO:", titulo)
            print("PREÇO:", preco)
            print("CATEGORIA:", categoria_preco)
            print("RELEVANTE:", relevante)
            print("LINK:", link)

            encontrados += 1

        except Exception:
            pass

    return resultados


def criar_bot(headless=False):
    bot = WebBot()
    bot.headless = headless
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()
    return bot


def buscar_em_farmacia(bot, medicamento, localizacao, farmacia, limite=10):
    resultados = []

    nome = farmacia["nome"]
    url_base = farmacia["url"]

    try:
        busca = quote_plus(medicamento)
        url = url_base.format(busca=busca)

        print("=" * 70)
        print(f"Pesquisando {medicamento} em {nome}...")
        print(url)
        print("=" * 70)

        bot.browse(url)
        time.sleep(8)

        resultados = coletar_links_pagina(
            bot=bot,
            medicamento=medicamento,
            localizacao=localizacao,
            farmacia_nome=nome,
            limite=limite
        )

        print(f"{nome}: {len(resultados)} resultados encontrados.")

    except Exception as erro:
        print(f"Erro na farmácia {nome}:", erro)

    return resultados


def buscar_medicamento(medicamento, localizacao):
    bot = criar_bot(headless=False)

    resultados = []

    try:
        for farmacia in FARMACIAS:
            try:
                resultados_farmacia = buscar_em_farmacia(
                    bot=bot,
                    medicamento=medicamento,
                    localizacao=localizacao,
                    farmacia=farmacia,
                    limite=10
                )

                resultados.extend(resultados_farmacia)

                time.sleep(3)

            except Exception as erro:
                print("Erro ao processar farmácia:", farmacia["nome"], erro)

    finally:
        try:
            bot.stop_browser()
        except Exception:
            pass

    salvar_resultados(resultados)

    return resultados


def montar_resposta(medicamento, localizacao, resultados):
    if not resultados:
        return (
            "💊 MediAlert AM\n\n"
            f"Nenhum resultado encontrado para: {medicamento}\n"
            f"📍 Local informado: {localizacao}"
        )

    resposta = (
        "💊 MediAlert AM\n\n"
        f"🔎 Medicamento: {medicamento}\n"
        f"📍 Local informado: {localizacao}\n\n"
    )

    for item in resultados[:12]:
        resposta += (
            f"🏥 {item['farmacia']}\n"
            f"Produto: {item['titulo']}\n"
            f"Preço: {item['preco']}\n"
            f"Categoria: {item['categoria_preco']}\n"
            f"Relevante: {item['relevante']}\n"
            f"Link: {item['link']}\n\n"
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

    resposta = requests.get(
        url,
        params=params,
        timeout=40
    )

    return resposta.json()


def main():
    print("MediAlert AM Telegram iniciado...")
    print("Envie no Telegram: medicamento | localização")
    print("Exemplo: dipirona | Centro Manaus")

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
                        "Envie no formato:\nmedicamento | localização\n\nExemplo:\ndipirona | Centro Manaus"
                    )
                    continue

                medicamento, localizacao = texto.split("|", 1)

                medicamento = medicamento.strip().lower()
                localizacao = localizacao.strip()

                enviar_mensagem(
                    chat_id,
                    f"🔎 Buscando {medicamento} próximo de {localizacao}..."
                )

                resultados = buscar_medicamento(
                    medicamento,
                    localizacao
                )

                resposta = montar_resposta(
                    medicamento,
                    localizacao,
                    resultados
                )

                enviar_mensagem(
                    chat_id,
                    resposta
                )

        except Exception as erro:
            print("Erro geral:", erro)
            time.sleep(5)


if __name__ == "__main__":
    main()