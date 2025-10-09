import json
import mysql.connector
import paho.mqtt.client as mqtt

print("📡 Script iniciado")

# --- Conexión a MySQL ---


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # ⚠ Poné tu contraseña si la tenés
        database="iot_systemsensor"
    )


db = connect_db()

# ID del sensor (según la tabla sensors)
SENSOR_ID = 1

# --- Callback al recibir mensaje MQTT ---
def on_message(client, userdata, msg):
    global db
    try:
        # Decodificar JSON
        data = json.loads(msg.payload.decode())
        nivel = data.get("nivel")
        alerta = data.get("alerta")
        estado = data.get("estado", "ok")

        # Guardar en MySQL
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO measurements (sensor_id, nivel, alerta, estado) VALUES (%s, %s, %s, %s)",
            (SENSOR_ID, nivel, alerta, estado)
        )
        db.commit()
        cursor.close()

        print("💾 Guardado en MySQL:", data)

    except mysql.connector.Error as e:
        print("❌ Error MySQL:", e)
        # Reintentar conexión si se pierde
        try:
            db = connect_db()
            print("🔄 Reconectado a MySQL")
        except Exception as ex:
            print("⛔ No se pudo reconectar a MySQL:", ex)
    except Exception as e:
        print("❌ Error procesando mensaje:", e)


# --- Configuración cliente MQTT ---
client = mqtt.Client()
client.on_message = on_message

# Conectar al broker público
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("iot/water")

print("🚀 Escuchando el tópico 'iot/water' y guardando en MySQL...")
client.loop_forever()
