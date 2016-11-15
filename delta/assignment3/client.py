import socket

# Create a TCP/IP socket
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8080)
sck.connect(server_address)

url = input("URL: ")
url += "\r\n"

#bytes and utf-8 is necessary for python 3.5
sck.send(bytes(url,'utf-8'))

sck.close()

