#include <WiFi.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ==========================================
// 1. CONFIGURAÇÕES DA SUA REDE WI-FI
// ==========================================
const char* ssid = "SEU_WIFI_AQUI";       
const char* password = "SUA_SENHA_AQUI";  

// ==========================================
// 2. CONFIGURAÇÕES DO SERVIDOR (IP)
// ==========================================
// No WINDOWS (CMD): Digite 'ipconfig' e procure por "Endereço IPv4"
// No LINUX/MAC (Terminal): Digite 'hostname -I' ou 'ifconfig'
const char* server_ip = "0.0.0.0"; // Substitua pelo IP do seu computador rodando o app.py

#define DHTPIN 4       
#define DHTTYPE DHT11  
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient mqttClient(espClient);

// ==========================================
// 3. ENDEREÇOS DE COMUNICAÇÃO (ROTAS)
// ==========================================
// Rota para o protocolo HTTP (API REST)
String http_url; 

// Canal (Tópico) para o protocolo MQTT
// Segue o padrão: área / projeto / dispositivo
String mqtt_topic = "iot/monitoramento/sensor";

bool usar_http = true; 

void setup() {
  Serial.begin(115200);
  dht.begin();

  http_url = String("http://") + server_ip + ":5000/dados_http";

  Serial.println("\nConectando ao WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Conectado! IP do ESP32: " + WiFi.localIP().toString());

  mqttClient.setServer(server_ip, 1883);
}

void reconectarMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Tentando conectar ao MQTT Broker... ");
    // Identificador genérico para o cliente MQTT
    if (mqttClient.connect("ESP32_Monitoramento_Cliente")) { 
      Serial.println("Conectado com sucesso!");
    } else {
      Serial.print("Falhou, erro=");
      Serial.print(mqttClient.state());
      Serial.println(" Tentando novamente em 5 segundos.");
      delay(5000);
    }
  }
}

void loop() {
  if (!mqttClient.connected()) {
    reconectarMQTT();
  }
  mqttClient.loop();

  // Ler o Sensor
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();

  // Tratamento em caso de mau contacto do sensor
  if (isnan(temp) || isnan(umid)) {
    Serial.println("Aviso: Falha ao ler o DHT11! A usar dados simulados de segurança...");
    temp = random(200, 300) / 10.0; 
    umid = random(400, 600) / 10.0; 
  }

  StaticJsonDocument<200> doc;
  doc["temp"] = temp;
  doc["umid"] = umid;
  
  unsigned long tempo_inicio = millis();
  unsigned long tempo_fim = 0;

  if (usar_http) {
    Serial.print("\nA enviar [HTTP] -> ");
    
    // Envia a latência real que foi medida no envio HTTP anterior!
    doc["latencia_ms"] = latencia_http_anterior; 
    String payload_http;
    serializeJson(doc, payload_http);
    Serial.println(payload_http);

    HTTPClient http;
    http.begin(http_url);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload_http);
    
    tempo_fim = millis();
    // Atualiza a latência real para o próximo envio
    latencia_http_anterior = tempo_fim - tempo_inicio;

    if (httpResponseCode > 0) {
      Serial.printf("Resposta HTTP: %d | Nova latência medida: %.2f ms\n", httpResponseCode, latencia_http_anterior);
    } else {
      Serial.printf("Erro no HTTP: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    http.end();
    
    usar_http = false;

  } else {
    Serial.print("\nA enviar [MQTT] -> ");
    
    // Envia a latência real que foi medida no envio MQTT anterior!
    doc["latencia_ms"] = latencia_mqtt_anterior; 
    String payload_mqtt;
    serializeJson(doc, payload_mqtt);
    Serial.println(payload_mqtt);

    bool sucesso = mqttClient.publish(mqtt_topic.c_str(), payload_mqtt.c_str());
    
    tempo_fim = millis();
    // Atualiza a latência real para o próximo envio
    latencia_mqtt_anterior = tempo_fim - tempo_inicio;

    if (sucesso) {
      Serial.printf("Publicado com sucesso | Nova latência medida: %.2f ms\n", latencia_mqtt_anterior);
    } else {
      Serial.println("Falha ao publicar no MQTT.");
    }
    
    usar_http = true;
  }

  Serial.println("A aguardar 10 segundos...\n");
  delay(10000); 
}
