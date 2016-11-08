# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 18:51:47 2016
"""

import socket
import json

# Create a TCP/IP socket
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8080)
sck.connect(server_address)

#try sending data and with the finally option, its used for clearing action that must happend after the try block ends
try:
    #Ask for input
    name = input("Name: ")
    age = input("Age: ")
    matrikelnummer = input("Matrikelnummer: ")
   
    # Build up JSON
    data = {}
    data['name'] = name
    data['age'] = age
    data['matrikelnummer'] = matrikelnummer
    json_data = json.dumps(data)
   
    # Send data
    sck.sendall(bytes(json_data,"UTF-8"))

finally:
	# Clean up the connection
    sck.close()
