print ("Scrip iniciado")
import paho.mqtt.client as mqtt
import mysql.connector
import json

# --- Conexión a MySQL ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="iot_systemsensor"
)
cursor = db.cursor()

# ID del sensor (según la tabla sensors, debería ser 1)
SENSOR_ID = 1

# --- Callback al recibir mensaje MQTT ---
def on_message(client, userdata, msg):
    try:
        # Decodificar el JSON
        data = json.loads(msg.payload.decode())
        nivel  = data.get("nivel")
        alerta = data.get("alerta")
        estado = data.get("estado", "ok")

        # Guardar en MySQL
        cursor.execute(
            "INSERT INTO measurements (sensor_id, nivel, alerta, estado) VALUES (%s, %s, %s, %s)",
            (SENSOR_ID, nivel, str(alerta), estado)
        )
        db.commit()

        print("💾 Guardado en MySQL:", data)

    except Exception as e:
        print("❌ Error procesando mensaje:", e)

# --- Configuración cliente MQTT ---
client = mqtt.Client()
client.on_message = on_message

# Usar el mismo broker que tu ESP32
client.connect("broker.hivemq.com, 1883, 60")
client.subscribe("iot/water")

print("🚀 Escuchando el tópico 'iot/water' y guardando en MySQL...")
client.loop_forever()
