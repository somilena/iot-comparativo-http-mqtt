"""
Projeto: Monitorização IoT - Comparativo HTTP vs MQTT
Autora: Milena
Ano: 2026
Descrição: Servidor back-end e API REST para telemetria IoT.
Este código é parte integrante de Trabalho de Conclusão de Curso (TCC).
Proibida a reprodução sem a manutenção dos devidos créditos
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Inicializa o servidor web Flask
app = Flask(__name__)
# O CORS é obrigatório para que o index.html consiga ler os dados sem bloqueios
CORS(app)

# Nome genérico para a base de dados
DB_NAME = 'banco_telemetria.db'

def init_db():
    """Cria a base de dados e a tabela de telemetria, se não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL,
            umidade REAL,
            protocolo TEXT,
            latencia_ms REAL,
            timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    conn.commit()
    conn.close()

def salvar_no_banco(t, u, p, l):
    """Guarda a leitura de temperatura, umidade e latência no SQLite."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leituras (temperatura, umidade, protocolo, latencia_ms) 
            VALUES (?, ?, ?, ?)
        """, (t, u, p, l))
        conn.commit()
        conn.close()
        print(f"[{p}] Dados Guardados -> Temp: {t}°C | Umid: {u}% | Latência: {l}ms")
    except Exception as e:
        print(f"Erro ao guardar na base de dados: {e}")

# ==========================================
# ROTAS DO SERVIDOR WEB (FLASK)
# ==========================================

@app.route('/')
def home():
    """Rota inicial só para confirmar que o servidor está online."""
    return "<h1>Servidor IoT de Monitoramento Ativo!</h1><p>O Back-end está a correr perfeitamente.</p>"

@app.route('/dados_http', methods=['POST'])
def receber_http():
    """Rota que recebe os dados do ESP32 via protocolo HTTP."""
    try:
        dados = request.get_json()
        salvar_no_banco(dados['temp'], dados['umid'], 'HTTP', dados['latencia_ms'])
        return jsonify({"status": "sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/ultimos_dados')
def ultimos_dados():
    """Rota que o index.html acede para montar os gráficos e a tabela."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Pega as últimas 30 linhas da base de dados
        cursor.execute("SELECT * FROM leituras ORDER BY id DESC LIMIT 30")
        rows = cursor.fetchall()
        conn.close()
        
        # Tratamento de dados (Garante que os números e datas estão formatados)
        dados_limpos = []
        for row in reversed(rows):
            d = dict(row)
            
            # Arredonda latência e valores para no máximo 2 casas decimais
            d['latencia_ms'] = round(float(d['latencia_ms'] or 0), 2)
            d['temperatura'] = round(float(d['temperatura'] or 0), 2)
            d['umidade'] = round(float(d['umidade'] or 0), 2)
            
            # Garante que o timestamp não é nulo (para não quebrar o JavaScript no gráfico)
            if not d.get('timestamp'):
                d['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            dados_limpos.append(d)
            
        return jsonify(dados_limpos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ==========================================
# CONFIGURAÇÃO DO BROKER MQTT
# ==========================================

def on_message(client, userdata, msg):
    """Função ativada automaticamente quando chega mensagem do ESP32 via MQTT."""
    try:
        dados = json.loads(msg.payload.decode())
        salvar_no_banco(dados['temp'], dados['umid'], 'MQTT', dados['latencia_ms'])
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

if __name__ == '__main__':
print("="*50)
print(" SISTEMA IoT - DESENVOLVIDO POR MILENA (TCC 2026) ")
print("="*50)
    
    # 1. Prepara a base de dados
    init_db()
    
    # 2. Tenta ligar ao Mosquitto (Broker MQTT)
    try:
        mqtt_client.connect("localhost", 1883, 60)
        # Tópico atualizado para coincidir com o código do ESP32
        mqtt_client.subscribe("iot/monitoramento/sensor")
        mqtt_client.loop_start()
        print("✅ Broker MQTT ligado e a aguardar dados...")
    except Exception as e:
        print(f"⚠️ Aviso: Mosquitto não encontrado. Erro: {e}")

    # 3. Inicia o servidor Flask na porta 5000, acessível na rede (0.0.0.0)
    print("🚀 A iniciar Servidor HTTP na porta 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
