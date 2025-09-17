
import paho.mqtt.client as mqtt
import mysql.connector
import json

# --- Configuración de MySQL ---
db = mysql.connector.connect(
    host="localhost",      # Si usás XAMPP, Laragon o MySQL local
    user="Grupoaprox",           # Tu usuario de MySQL
    password="Grupoaprox",           # Tu contraseña de MySQL 
    database="iot_systemsensor"  # Nombre de tu base
)
cursor = db.cursor()

# --- Callback cuando llega un mensaje ---
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        nivel = data.get("nivel")
        alerta = data.get("alerta")
        estado = data.get("estado")

        cursor.execute(
            "INSERT INTO water_level (nivel, alerta, estado) VALUES (%s, %s, %s)",
            (nivel, alerta, estado)
        )
        db.commit()
        print("💾 Guardado en MySQL:", data)

    except Exception as e:
        print("❌ Error al procesar mensaje:", e)

# --- Configuración MQTT ---
client = mqtt.Client()
client.connect("broker.emqx.io", 1883, 60)  # Broker público
client.subscribe("iot/water")
client.on_message = on_message

print("📡 Escuchando el tópico 'iot/water'...")
client.loop_forever()
