import socket

# Create a TCP/IP socket
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8080)
print ('starting up on %s port %s' % server_address)
sck.bind(server_address)

# Listen for incoming connections, the passed value indicates the maximum number of connections to be created at once
sck.listen(1)

#empty string to concatenate result in
result =""

while True:
    # Wait for a connection
    connection, client_address = sck.accept()
    #try receiving data and with the finally option, its used for clearing action that must happend after the try block ends
    try:
        print ( 'connection from', client_address)
        while True:
            data = connection.recv(1024)
			#bytes and utf-8 is necessary for python 3.5
            url = data.decode('utf-8')
			# if we got data process it else break the loop of waiting for data.
            if data:
                
                #splitting the url
                splitted = url.split(":")
                portPathParams = splitted[2].split("?")
                paramsFragment = portPathParams[1].split("#")
                domains = splitted[1].split(".")
                portPath = portPathParams[0].split("/")
                params = paramsFragment[0].split("&")
                
                #concatenating the final results in one string
                result += "Protocol: " + splitted[0] + "\n"
                result += "Domain: " + domains[1] + "." + domains[2] + "\n"
                result += "Sub-Domain: " + domains[0].split("//")[1] + "\n"
                result += "Port number: " + portPath[0] + "\n"
                result += "Path: " + portPath[1]+"/"+portPath[2]+"/"+portPath[3] + "\n"
                result += "Paramters: " + paramsFragment[0] + "\n"
                result += "Fragment: " + paramsFragment[1]
                print(result)
                    
            else:
                break
            
    finally:
        # Clean up the connection
        connection.close()