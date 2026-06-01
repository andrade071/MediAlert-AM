#  MediAlert AM

## Sistema Inteligente de Monitoramento de Medicamentos

###  Descrição

O MediAlert AM é um sistema de automação desenvolvido em Python para monitorar medicamentos em farmácias online. O sistema realiza pesquisas automáticas em diferentes drogarias, coleta informações dos produtos encontrados e envia notificações via Telegram para o usuário.

O objetivo é facilitar a busca por medicamentos, permitindo acompanhar disponibilidade e comparar resultados em diferentes farmácias de forma automatizada.

---

##  Objetivo

Desenvolver uma solução automatizada capaz de:

* Pesquisar medicamentos em farmácias online;
* Coletar informações dos produtos encontrados;
* Centralizar os resultados em um arquivo CSV;
* Enviar notificações automáticas pelo Telegram;
* Auxiliar usuários na localização de medicamentos em diferentes estabelecimentos.

---

##  Funcionalidades

### Pesquisa Automatizada

O sistema realiza buscas automáticas para medicamentos cadastrados.

Exemplos:

* Dipirona
* Loratadina
* Paracetamol

### Monitoramento Multicanal

Atualmente o sistema consulta:

* Drogasil
* Bemol Farma
* Pague Menos
* FarmaBem

### Armazenamento de Resultados

Os dados encontrados são armazenados em:

```text
resultados.csv
```

### Notificações em Tempo Real

Ao finalizar a execução, o sistema envia um resumo dos resultados diretamente para o Telegram.

### Geolocalização por Região

O sistema permite associar medicamentos a uma localização informada pelo usuário, facilitando futuras implementações de busca regionalizada.

---

## 🛠 Tecnologias Utilizadas

### Linguagem

* Python 3.11

### Automação Web

* BotCity Web
* Selenium

### Gerenciamento do ChromeDriver

* WebDriver Manager

### Manipulação de Dados

* Pandas

### Integração Telegram

* Requests
* Python Dotenv

---

##  Estrutura do Projeto

```text
medicamento/
│
├── bot.py
├── medicamentos.csv
├── resultados.csv
├── .env
├── requirements.txt
└── README.md
```

---

##  Instalação

### 1. Clonar o projeto

```bash
git clone <url-do-repositorio>
```

### 2. Acessar a pasta

```bash
cd medicamento
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

##  Configuração do Telegram

Criar um arquivo:

```text
.env
```

Conteúdo:

```env
TELEGRAM_TOKEN=SEU_TOKEN
TELEGRAM_CHAT_ID=SEU_CHAT_ID
```

---

##  Arquivo de Medicamentos

Criar o arquivo:

```text
medicamentos.csv
```

Exemplo:

```csv
medicamento,preco_maximo,localizacao
dipirona,15.00,Adrianópolis Manaus
loratadina,20.00,Cidade Nova Manaus
paracetamol,12.00,Centro Manaus
```

---

## ▶ Execução

Executar:

```bash
python bot.py
```

O sistema irá:

1. Abrir o navegador;
2. Pesquisar os medicamentos;
3. Coletar os resultados;
4. Salvar o CSV;
5. Enviar notificação pelo Telegram.

---

##  Exemplo de Saída

```text
 MediAlert AM - Resultado da busca

 Dipirona
- Drogasil
- Bemol Farma

 Loratadina
- Drogasil
- Pague Menos
```

---

##  Melhorias Futuras

* Captura automática de preços reais;
* Comparação de preços entre farmácias;
* Geolocalização por GPS;
* Dashboard Web;
* Integração com Google Maps;
* Histórico de preços;
* Aplicativo Mobile;
* Alertas inteligentes por faixa de preço.

---

## 👩 Desenvolvedora

**Raquel Andrade da Gama**

Tecnóloga em Análise e Desenvolvimento de Sistemas.

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e educacionais.
