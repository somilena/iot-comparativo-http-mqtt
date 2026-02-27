import requests
import time
import random
import json
import paho.mqtt.client as mqtt

# Configurações
SERVER_URL = "http://localhost:5000/api/dados"
MQTT_BROKER = "localhost" # ou o endereço do seu broker
MQTT_TOPIC = "casa/monitoramento"

def simular_http():
    payload = {
        "sensor_id": "ESP32_Simulado",
        "temperatura": round(random.uniform(20.0, 30.0), 2),
        "umidade": round(random.uniform(40.0, 70.0), 2),
        "protocolo": "HTTP"
    }
    try:
        inicio = time.time()
        response = requests.post(SERVER_URL, json=payload)
        fim = time.time()
        print(f"[HTTP] Status: {response.status_code} | Latência: {fim-inicio:.4f}s")
    except Exception as e:
        print(f"[HTTP] Erro: {e}")

def simular_mqtt(client):
    payload = {
        "sensor_id": "ESP32_Simulado",
        "temperatura": round(random.uniform(20.0, 30.0), 2),
        "umidade": round(random.uniform(40.0, 70.0), 2),
        "protocolo": "MQTT"
    }
    inicio = time.time()
    client.publish(MQTT_TOPIC, json.dumps(payload))
    fim = time.time()
    print(f"[MQTT] Enviado | Latência: {fim-inicio:.4f}s")

if __name__ == "__main__":
    # Setup MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    
    print("Iniciando simulação de dados (Ctrl+C para parar)...")
    try:
        while True:
            # Alterna entre protocolos para comparação
            simular_http()
            time.sleep(2)
            simular_mqtt(mqtt_client)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nSimulação finalizada.")
