from telegram_bot import buscar_medicamento
import time


medicamentos = [
    "dipirona", "paracetamol", "loratadina", "ibuprofeno",
    "omeprazol", "losartana", "dorflex", "neosaldina",
    "vitamina c", "nimesulida", "simeticona", "buscopan",
    "cetirizina", "allegra", "tylenol", "novalgina",
    "benegrip", "cimegripe", "dramim", "sonrisal",
    "amitriptilina", "metformina", "sinvastatina", "atenolol",
    "enalapril", "hidroclorotiazida", "azitromicina", "amoxicilina",
    "fluconazol", "prednisona", "dexclorfeniramina", "desloratadina",
    "fexofenadina", "diclofenaco", "naproxeno", "cetoprofeno",
    "pantoprazol", "domperidona", "clonazepam", "sertralina"
]

locais = [
    "Centro Manaus", "Adrianópolis Manaus", "Cidade Nova Manaus",
    "Alvorada Manaus", "Flores Manaus", "Compensa Manaus",
    "Aleixo Manaus", "Tarumã Manaus", "Ponta Negra Manaus",
    "Parque 10 Manaus"
]


for medicamento in medicamentos:
    for local in locais:
        print("=" * 60)
        print(f"Coletando: {medicamento} | {local}")
        print("=" * 60)

        try:
            buscar_medicamento(medicamento, local)
        except Exception as erro:
            print("Erro na coleta:", erro)

        time.sleep(2)


print("Coleta automática finalizada.")