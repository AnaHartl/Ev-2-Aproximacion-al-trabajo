import json
import time
import paho.mqtt.client as mqtt
import mysql.connector

# --- Configuración de conexión ---
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "iot/water"  # mismo que el ESP32
CLIENT_ID = f"pc_mysql_listener_{int(time.time())}"

# --- Conexión a MySQL ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anita2701",  # ⚠️ tu contraseña de MySQL
        database="iot_systemsensor"
    )

# Intentar conectar al iniciar
try:
    db = connect_db()
    print("✅ Conectado a MySQL")
except Exception as e:
    print("❌ Error conectando a MySQL:", e)
    db = None


# --- Callbacks MQTT ---
def on_connect(client, userdata, flags, rc):
    print(f"✅ MQTT conectado (rc={rc})")
    client.subscribe(TOPIC)
    print(f"📥 Suscripto a {TOPIC}")


def on_disconnect(client, userdata, rc):
    print(f"⚠️ MQTT desconectado (rc={rc})")


def on_message(client, userdata, msg):
    global db
    try:
        payload = msg.payload.decode(errors="ignore")
        data = json.loads(payload)
        print(f"📩 Recibido: {data}")

        # Extraer valores
        sensor_id = 1
        nivel = data.get("nivel", 0)
        alerta = data.get("alerta", 0)
        estado = data.get("estado", "ok")

        # Guardar en MySQL
        if db is None or not db.is_connected():
            db = connect_db()

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO measurements (sensor_id, nivel, alerta, estado)
            VALUES (%s, %s, %s, %s)
        """, (sensor_id, nivel, alerta, estado))
        db.commit()
        cursor.close()

        print("💾 Guardado en MySQL correctamente")

    except mysql.connector.Error as e:
        print("❌ Error MySQL:", e)
        db = None  # Fuerza reconexión en el siguiente ciclo
    except json.JSONDecodeError:
        print("⚠️ Error al decodificar JSON:", msg.payload)
    except Exception as e:
        print("⚠️ Error procesando mensaje:", e)


# --- Configuración del cliente MQTT ---
client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.reconnect_delay_set(min_delay=1, max_delay=10)

# --- Ejecutar ---
print("🚀 Iniciando script MQTT → MySQL")
client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
