"""
Projeto: Monitorização IoT - Comparativo HTTP vs MQTT
Autora: Milena
Ano: 2026
Descrição: Servidor back-end e API REST para telemetria IoT.
Este código é parte integrante de Trabalho de Conclusão de Curso (TCC).
Proibida a reprodução sem a manutenção dos devidos créditos.
"""

import requests
import time
import random
import json
import paho.mqtt.client as mqtt

# Configurações CORRIGIDAS para bater com o app.py
SERVER_URL = "http://localhost:5000/dados_http"
MQTT_BROKER = "localhost" 
MQTT_TOPIC = "iot/monitoramento/sensor"

def simular_http():
    # Chaves atualizadas para temp, umid e latencia_ms
    payload = {
        "temp": round(random.uniform(20.0, 30.0), 2),
        "umid": round(random.uniform(40.0, 70.0), 2),
        "latencia_ms": round(random.uniform(15.0, 45.0), 2) # Simulando latência HTTP
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        print(f"[HTTP] Status: {response.status_code} | Dados: {payload}")
    except Exception as e:
        print(f"[HTTP] Erro: {e}")

def simular_mqtt(client):
    payload = {
        "temp": round(random.uniform(20.0, 30.0), 2),
        "umid": round(random.uniform(40.0, 70.0), 2),
        "latencia_ms": round(random.uniform(5.0, 15.0), 2) # Simulando latência MQTT (geralmente menor)
    }
    client.publish(MQTT_TOPIC, json.dumps(payload))
    print(f"[MQTT] Enviado com sucesso | Dados: {payload}")

if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    
    print("Iniciando simulação de dados (Ctrl+C para parar)...")
    try:
        while True:
            simular_http()
            time.sleep(2)
            simular_mqtt(mqtt_client)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nSimulação finalizada.")
