import bluetooth
import random
import time
import dht
import machine
from machine import Pin
from simpleBLE import BLEPeripheral

# Bluetooth object
ble = bluetooth.BLE() 

# Environmental service
service= "1577e6c1-a501-41c5-8d0d-cca65eabc253" 

# Temperature characteristic
characteristic="248fa813-6cf6-44a0-b5f5-d6dcad476d91"



# BLE peripheral object
sensor = BLEPeripheral(ble,"sensor",service,characteristic)  

d = dht.DHT11(Pin(15))

i = 0
#using deepsleep method
while True:
    i = (i + 1) % 10
    d.measure()
    temperature = d.temperature()
    humidity = d.humidity()
    print('Temperature: {}°C\tHumidity: {}%'.format(temperature, humidity))
    sensor.set_values([int(temperature*100), int(humidity*100)], notify= i, indicate=False)
    time.sleep_ms(1000)
