from telegram_bot import buscar_medicamento
import time


medicamentos = [
    "dipirona",
    "paracetamol",
    "loratadina",
    "ibuprofeno",
    "omeprazol",
    "losartana",
    "dorflex",
    "neosaldina",
    "vitamina c",
    "nimesulida",
    "amitriptilina",
    "metformina",
    "sinvastatina",
    "atenolol",
    "amoxicilina"
]


bairros_extra = [
    "Zumbi Manaus",
    "Jorge Teixeira Manaus",
    "Santo Agostinho Manaus",
    "Mauazinho Manaus",
    "São José Manaus",
    "Coroado Manaus",
    "Educandos Manaus",
    "Cachoeirinha Manaus",
    "Colônia Terra Nova Manaus",
    "Novo Aleixo Manaus",
    "Monte das Oliveiras Manaus",
    "Redenção Manaus",
    "Japiim Manaus",
    "São Raimundo Manaus",
    "Dom Pedro Manaus"
]


for bairro in bairros_extra:
    for medicamento in medicamentos:
        print("=" * 60)
        print(f"Coletando: {medicamento} | {bairro}")
        print("=" * 60)

        try:
            buscar_medicamento(medicamento, bairro)
        except Exception as erro:
            print("Erro na coleta:", erro)

        time.sleep(2)


print("Coleta extra por bairros finalizada.")