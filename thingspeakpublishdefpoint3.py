from os import statvfs
from time import sleep
import network
from mqtt import MQTTClient 
import machine 
import time
import json
import struct
from micropython import const
import bluetooth
from simpleBLE import BLECentral 

# MQTT credentials
USERNAME = const('FxghKRgFBiouASo5DR8XBC0')
CLIENTID = const('FxghKRgFBiouASo5DR8XBC0')
PASS = const('3YxdpKAlJHUaNRYgxoHsoKJ1')
SERVER=const('mqtt3.thingspeak.com')
CHANNEL=const('2052992')

# BLE credentials
service="1577e6c1-a501-41c5-8d0d-cca65eabc253"
characteristic="248fa813-6cf6-44a0-b5f5-d6dcad476d91"

def free_flash():
  s = statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

def sub_cb(topic, msg):
    print(msg[0])   
    if msg[0]==48:
       led.value(0)
    elif msg[0]==49:
        led.value(1)

print('Available flash memory: '+free_flash())

# Initialize LED
led = machine.Pin(2,machine.Pin.OUT)

# Connect to MQTT broker and subscribe to channel
client = MQTTClient(client_id=CLIENTID, server=SERVER, user=CLIENTID, password=PASS)
client.set_callback(sub_cb) 
client.connect()
client.subscribe(topic='channels/'+CHANNEL+'/subscribe/fields/field1')

# Connect to BLE temperature and humidity sensor
ble = bluetooth.BLE()
central = BLECentral(ble, service, characteristic)
not_found = False

def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        central.connect()
    else:
        global not_found
        not_found = True
        print("No sensor found.")

central.scan(callback=on_scan)

# Wait for connection...
while not central.is_connected():
    time.sleep_ms(100)
    if not_found:
        sys.exit()

print("Connected")

# Publish temperature and humidity readings to Thingspeak channel
while central.is_connected():
    central.read(callback=lambda data: client.publish(topic="channels/"+CHANNEL+"/publish", msg='field1={0:.0f}&field2={1:.0f}'.format(data[0]/100, data[1]/100)))
    #client.check_msg()
    time.sleep_ms(2000)

print("Disconnected")
