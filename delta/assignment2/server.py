# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 18:49:04 2016
"""

import socket
import json

# Create a TCP/IP socket
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8080)
print ('starting up on %s port %s' % server_address)
sck.bind(server_address)

# Listen for incoming connections,
#the passed value indicates the maximum number
#of connections to be created at once
sck.listen(1)

while True:
    # Wait for a connection
    connection, client_address = sck.accept()
    #try receiving data and with the finally option,
	#its used for clearing action that must happend after the try block ends
    try:
        print ( 'connection from', client_address)
        while True:
            data = connection.recv(1024)
			#if we got data process it
			#else break the loop of waiting for data.
            if data:
                final_data = json.loads(data.decode("utf-8"))
                print('Name:' + final_data['name']+ ';')
                print('Age:' + final_data['age']+ ';')
                print('Matrikelnummer:' + final_data['matrikelnummer']) 
            else:
                break
            
    finally:
        # Clean up the connection
        connection.close()