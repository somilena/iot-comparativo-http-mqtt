
# 🏠 Monitorização IoT: Comparativo de Performance HTTP vs MQTT

Este repositório contém o código-fonte desenvolvido para o Trabalho de Conclusão de Curso (TCC) em Engenharia da Computação. O projeto consiste em um sistema completo de telemetria IoT utilizando um **ESP32**, que coleta, armazena e exibe dados de temperatura e umidade. O objetivo principal é comparar a latência, a confiabilidade e a eficiência entre os protocolos **HTTP** e **MQTT**.

---

## 📑 Índice
- [Visão Geral](#-visão-geral)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)
- [Pré-requisitos](#-pré-requisitos)
- [Como Executar](#-como-executar)
- [Autora](#-autora)

---

## 🎯 Visão Geral
Em aplicações de Internet das Coisas (IoT), a escolha do protocolo de comunicação é crucial para o desempenho do sistema. Este projeto utiliza um ESP32 programado em C++ para enviar pacotes de dados alternando entre requisições HTTP e publicações MQTT. 

A aplicação conta com um painel web responsivo que consome uma API local em Flask para exibir:
- Telemetria em tempo real (Temperatura e Umidade).
- Gráficos comparativos de latência (ms) entre os dois protocolos.
- Histórico completo de logs persistidos em um banco de dados SQLite3.

---

## 🏗️ Arquitetura do Projeto

1. **Firmware (`monitoramento.ino`):** Código em C++ embarcado no ESP32, responsável pela leitura dos sensores e envio dos dados via Wi-Fi usando HTTP e MQTT.
2. **Servidor Backend (`app.py`):** Aplicação em Python (Flask) que atua como API REST para o dashboard e gerencia a gravação dos dados no SQLite.
3. **Simulador (`simulador.py`):** Script em Python para gerar dados fictícios e testar a infraestrutura sem a necessidade do hardware físico.
4. **Dashboard (`index.html`):** Interface visual construída com HTML, Tailwind CSS e Chart.js que consome os dados do backend.

---

## 📂 Estrutura de Arquivos

```text
iot-comparativo-http-mqtt/
├── firmware/
│   └── monitoramento.ino      # Código para o ESP32 (C++)
├── server/
│   ├── app.py                 # Servidor Flask (API e integração MQTT)
│   └── simulador.py           # Script para testar a comunicação sem hardware
├── dashboard/
│   └── index.html             # Interface Web de monitoramento
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências do Python
└── .gitignore                 # Arquivos e pastas ignorados pelo Git
```

## ⚙️ Pré-requisitos
```text
Para rodar este projeto localmente, você precisará de:
Python 3.8+
Um Broker MQTT local ou em nuvem (ex: Eclipse Mosquitto)
IDE Arduino (para compilar e gravar o código no ESP32)
Bibliotecas do ESP32 instaladas na IDE Arduino (PubSubClient, HTTPClient, WiFi)
```

## 🚀 Como Executar

1. Clonando o Repositório
```text
git clone [https://github.com/SEU_USUARIO/iot-comparativo-http-mqtt.git](https://github.com/SEU_USUARIO/iot-comparativo-http-mqtt.git)
cd iot-comparativo-http-mqtt
```

2. Configurando o Servidor Python
Recomenda-se o uso de um ambiente virtual (venv).

# Instale as dependências
```text
pip install -r requirements.txt
```

# Inicie a API Flask
```text
python server/app.py
```

3. Testando com o Simulador (Opcional)
Caso não esteja com o ESP32 conectado, você pode gerar dados de teste:

```text
python server/simulador.py
```

4. Acessando o Dashboard
Abra o arquivo dashboard/index.html em seu navegador. Insira o IP do servidor (ou mantenha localhost) e clique em CONECTAR para visualizar o fluxo de dados.


## 👩‍💻 Autora
```text
Milena
Estudante de Engenharia da Computação
Desenvolvedora principal do projeto de TCC.
```

