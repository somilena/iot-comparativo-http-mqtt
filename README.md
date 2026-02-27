# 🏠 Monitorização IoT: Comparativo de Performance HTTP vs MQTT

Este repositório contém o código-fonte desenvolvido para o Trabalho de Conclusão de Curso (TCC) em Engenharia de Computação. O projeto consiste em um sistema completo de telemetria IoT utilizando um **ESP32**, que coleta, armazena e exibe dados de temperatura e umidade. O objetivo principal é comparar a latência, a confiabilidade e a eficiência entre os protocolos **HTTP** e **MQTT**.

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
├── LICENSE                    # Licença MIT de uso e direitos autorais
├── requirements.txt           # Dependências do Python
└── .gitignore                 # Arquivos e pastas ignorados pelo Git
```

---

## ⚙️ Pré-requisitos
Para rodar este projeto localmente, você precisará de:

* Python 3.8+
* Um Broker MQTT local ou em nuvem (ex: Eclipse Mosquitto)
* IDE Arduino (para compilar e gravar o código no ESP32)
* Bibliotecas do ESP32 instaladas na IDE Arduino (`PubSubClient`, `HTTPClient`, `WiFi`)

---

## 🚀 Como Executar

### 1. Clonando o Repositório
Antes de iniciar, certifique-se de que possui o [Git](https://git-scm.com/downloads) instalado em sua máquina. 

Abra o seu terminal e execute o comando abaixo para baixar o código:
```bash
git clone https://github.com/somilena/iot-comparativo-http-mqtt.git
```

Após a conclusão do download, acesse a pasta recém-criada do projeto:
```bash
cd iot-comparativo-http-mqtt
```

### 2. Configurando o Servidor Python
Para evitar conflitos com os pacotes do sistema operacional (evitando o erro de *externally-managed-environment*), é altamente recomendado o uso de um ambiente virtual isolado (`venv`).

Crie o ambiente virtual:
```bash
python3 -m venv venv
```

Em seguida, ative o ambiente virtual de acordo com o seu sistema operacional:

* 🐧 **Linux e macOS:**
  ```bash
  source venv/bin/activate
  ```
* 🪟 **Windows (Prompt de Comando/PowerShell):**
  ```bash
  venv\Scripts\activate
  ```

Com o ambiente virtual ativado (você verá a indicação `(venv)` no início da linha do terminal), instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

Por fim, inicie a API Flask e o cliente MQTT:
```bash
python server/app.py
```

### 3. Testando com o Simulador (Opcional)
Caso não possua o hardware (ESP32) conectado no momento, você pode gerar dados de teste para visualizar o funcionamento do sistema. 

Abra um **novo terminal** (deixe o servidor Flask rodando no anterior), acesse a pasta do projeto e ative o ambiente virtual:
```bash
cd iot-comparativo-http-mqtt
```

* 🐧 **Linux e macOS:**
  ```bash
  source venv/bin/activate
  ```
* 🪟 **Windows:**
  ```bash
  venv\Scripts\activate
  ```

Em seguida, execute o script do simulador:
```bash
python server/simulador.py
```
> 💡 *O simulador começará a enviar pacotes fictícios alternando entre HTTP e MQTT. Deixe este terminal aberto executando em segundo plano.*

### 4. Acessando o Dashboard
Para garantir que os gráficos e bibliotecas externas carreguem corretamente sem bloqueios de segurança do navegador, iniciaremos um servidor local leve para o front-end.

Abra um **terceiro terminal** e acesse diretamente a pasta do dashboard:
```bash
cd iot-comparativo-http-mqtt/dashboard
```

Inicie o servidor web nativo do Python:

* 🐧 **Linux e macOS:**
  ```bash
  python3 -m http.server 8000
  ```
* 🪟 **Windows:**
  ```bash
  python -m http.server 8000
  ```

Abra o seu navegador web e acesse o endereço: **`http://localhost:8000`**

Quando a interface carregar, insira o IP do servidor back-end (ou mantenha `localhost`) no campo superior direito e clique em **CONECTAR** para visualizar o fluxo de dados em tempo real.

### 5. Acessando a API Diretamente (Dados Brutos)
Como a arquitetura foi desenvolvida no padrão REST, o servidor Flask atua de forma independente do dashboard. Para fins de análise e validação acadêmica, você pode acessar os endpoints da API diretamente pelo navegador e visualizar o formato JSON puro.

**Acesso na própria máquina (Localhost):**
* **Status do Servidor:** Acesse `http://localhost:5000/`
* **Dados JSON (Telemetria):** Acesse `http://localhost:5000/ultimos_dados` para visualizar os últimos 30 registros persistidos no SQLite.

**Acesso através de outros dispositivos (Mesma rede Wi-Fi):**
Como a API está configurada para ouvir em `0.0.0.0`, você pode acessar os dados através de um celular ou outro computador conectado à mesma rede. Basta substituir `<SEU_IP>` pelo endereço IPv4 exibido no terminal quando o Flask é iniciado (ex: `192.168.1.15`):
* **Status do Servidor:** Acesse `http://<SEU_IP>:5000/`
* **Dados JSON (Telemetria):** Acesse `http://<SEU_IP>:5000/ultimos_dados`

---

## 👩‍💻 Autora

**Milena**
* Estudante de Engenharia de Computação
* Desenvolvedora principal do projeto de TCC.
