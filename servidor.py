import paho.mqtt.client as mqtt
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

conn = sqlite3.connect('sensores.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS dados_sensores
             (timestamp TEXT, temperatura REAL, umidade REAL, pressao REAL)''')
conn.commit()

temperaturas = []
umidades = []
pressoes = []
tempos = []

def on_connect(client, userdata, flags, rc):
    print(f"Conectado com o código: {rc}")
    client.subscribe("sensor/temperatura")
    client.subscribe("sensor/umidade")
    client.subscribe("sensor/pressao")

def on_message(client, userdata, msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if msg.topic == "sensor/temperatura":
        temperatura = float(msg.payload.decode())
        temperaturas.append(temperatura)
        if len(temperaturas) > len(tempos):
            tempos.append(timestamp)
        c.execute("INSERT INTO dados_sensores (timestamp, temperatura) VALUES (?, ?)", (timestamp, temperatura))
    elif msg.topic == "sensor/umidade":
        umidade = float(msg.payload.decode())
        umidades.append(umidade)
        if len(umidades) > len(tempos):
            tempos.append(timestamp)
        c.execute("INSERT INTO dados_sensores (timestamp, umidade) VALUES (?, ?)", (timestamp, umidade))
    elif msg.topic == "sensor/pressao":
        pressao = float(msg.payload.decode())
        pressoes.append(pressao)
        if len(pressoes) > len(tempos):
            tempos.append(timestamp)
        c.execute("INSERT INTO dados_sensores (timestamp, pressao) VALUES (?, ?)", (timestamp, pressao))

    conn.commit()

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

def atualizar_grafico(frame):
    plt.clf()

    if len(tempos) == len(temperaturas):
        plt.subplot(3, 1, 1)
        plt.plot(tempos, temperaturas, label="Temperatura (ºC)", color="red")
        plt.legend(loc="upper right")

    if len(tempos) == len(umidades):
        plt.subplot(3, 1, 2)
        plt.plot(tempos, umidades, label="Umidade (%)", color="blue")
        plt.legend(loc="upper right")

    if len(tempos) == len(pressoes):
        plt.subplot(3, 1, 3)
        plt.plot(tempos, pressoes, label="Pressão (hPa)", color="green")
        plt.legend(loc="upper right")

    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), atualizar_grafico, interval=1000)

client.loop_start()

plt.show()

client.loop_stop()
conn.close()