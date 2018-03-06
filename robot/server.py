#!/usr/bin/python3

# A tiny server using asynchronous sockets
#
# This micro server communicates with a robot and transmits the data
# to a Cayenne dashboard.
# The Raspberry Pi listens on the Ethernet interface, and then
# transmits the data via Wifi.
#
# Author: J. Barthelemy and G. Michal
# Version: 1.0


import asyncio
import struct
import math
import textwrap

import cayenne.client
import time
import threading

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
threading.Timer(1, connect_cayenne_forever).start()
    
# Micro server receing data from the Robot
class ServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        print(len(data))
        print(data)
        
        # decoding the message
        message = data.decode()        
        print('Data received: {!r}'.format(message))            
        value = int(message)
        print('Data decoded: {}'.format(value))
                
        # sending the message via MQQT
        # client.loop()    
        channel = 1        
        client.virtualWrite(channel, value)
       
        # closing the client socket
        print('Close the client socket')
        self.transport.close()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(ServerClientProtocol, '192.168.2.20', 6000)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
