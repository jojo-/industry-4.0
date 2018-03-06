#!/usr/bin/python3

# A tiny server using asynchronous sockets
#
# Read the data from an air compressor by using the Modbus protocol.
# The data is then send to a Cayenne Dashboard.

# Author: J. Barthelemy and G. Michal
# Version: 1.0

# Note Incoming data should be encoded using big endian!


import cayenne.client
import threading
import minimalmodbus
import random

SAMPLING_INTERVAL = 15

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "XXX"
MQTT_PASSWORD  = "YYY"
MQTT_CLIENT_ID = "ZZZ"

# Connecting to Cayenne
print("Connecting to Cayenne...")
client = cayenne.client.CayenneMQTTClient()
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
print("Done!")

# Reconnect to Cayenne every 45 seconds
def connect_cayenne_forever():
    print("Keeping the connection to Cayenne...")
    client.loop_forever()
    #threading.Timer(45, reconnect_cayenne).start()    

def collect_and_send_data():
    
    print("Collecting and sending data")
    
    try:
        # connection to the air compressor
        instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

	# pressure stage 1 output
        channel_pressure_stage1_out = 1
        pressure_stage1_out = instrument.read_register(46, 1)
        pressure_stage1_out = instrument.read_register(46, 1)
        client.virtualWrite(channel_pressure_stage1_out, pressure_stage1_out, dataType="bp",dataUnit="hpa")
        #value_temp = random.randint(0,100)
        #client.celsiusWrite(channel_temp, value_temp)

        # pressure line
        channel_pressure_line = 2
        pressure_line = instrument.read_register(47, 1)
        pressure_line = instrument.read_register(47, 1)
        client.virtualWrite(channel_pressure_line, pressure_line, dataType="bp",dataUnit="hpa")
        #value_pressure = random.randint(0,100)
        #client.pascalWrite(channel_pressure, value_pressure)

        # temperature stage 1 output
        channel_temperature_stage1_out = 3
        temperature_stage1_out = instrument.read_register(48, 1)
        temperature_stage1_out = instrument.read_register(48, 1)
        client.virtualWrite(channel_temperature_stage1_out, temperature_stage1_out, dataType="temp", dataUnit="c")

        # running hours
        # channel_running_hours = 4
        running_hours = instrument.read_register(58, 1)
        running_hours = instrument.read_register(58, 1)
        # client.virtualWrite(channel_running_hours, running_hours)

        # loaded hours
        # channel_loaded_hours = 5
        loaded_hours = instrument.read_register(60, 1)
        loaded_hours = instrument.read_register(60, 1)
        # client.virtualWrite(channel_loaded_hours, loaded_hours)

        channel_ratio_hours = 6
        ratio_hours = loaded_hours / running_hours
        client.virtualWrite(channel_ratio_hours, ratio_hours, dataType="counter", dataUnit="null")

    except:
        print("Could not connect with the device!")

    # schedule next data collection
    threading.Timer(SAMPLING_INTERVAL, collect_and_send_data).start()


threading.Timer(1, connect_cayenne_forever).start()
threading.Timer(5, collect_and_send_data).start()
