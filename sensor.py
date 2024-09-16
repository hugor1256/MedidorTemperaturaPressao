import paho.mqtt.client as mqtt
import time
import random

client = mqtt.Client()

client.connect("broker.hivemq.com", 1883, 60)

while True:
    temperatura = random.uniform(20.0, 30.0)
    umidade = random.uniform(30.0, 60.0)
    pressao = random.uniform(900.0, 1100.0)
    
    client.publish("sensor/temperatura", f"{temperatura:.2f}")
    client.publish("sensor/umidade", f"{umidade:.2f}")
    client.publish("sensor/pressao", f"{pressao:.2f}")
    
    print(f"Temperatura: {temperatura:.2f} ºC, Umidade: {umidade:.2f} %, Pressão: {pressao:.2f} hPa")
    
    time.sleep(5)