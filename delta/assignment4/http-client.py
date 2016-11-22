import socket
from urllib.parse import urlparse
import time


# function to separate header from body & print header to console
# also save body in the appropriate file format according to the
# content type value of the header
def getHeaderAndBody(receivedData, fPath):
    # find the starting part of body
    startOfBody = receivedData.find(b"\r\n\r\n")
    # creating the header part
    header = receivedData[:startOfBody]
    # creating the body part
    # the constant 4 is just to escape the \r\n\r\n characters
    body = receivedData[(startOfBody + 4):]

    # if the HTTP status is 200 OK we process header & body
    # else we just print out the header
    if (str(header)).find("200 OK") >= 0:
        # creating the header dictionary
        # to know the content type
        headerDictionary = createHeaderDict(header.decode("utf-8"))
        # extracting the content type of the body
        contentType = headerDictionary["Content-Type"]
        # getting the image name by splitting on the url path
        splittedPath = fPath.split("/")
        fileName = splittedPath[-1]
        # according to the content type
        # save the body in appropriate format
        if contentType.find("image") >= 0:
            # writing to the body file
            # which will be created if it doesn't exist
            # using 'wb' to write bytes to the file and not strings
            bodyFile = open(fileName, "wb")
            bodyFile.write(body)
            # writing to the header file
            # which will be created if it doesn't exist
            headerFile = open("image_header.txt", 'w')
            headerFile.write(header.decode("utf-8"))
        elif contentType.find("text/html") >= 0:
            # if the file name doesn't have extension we add it
            # using the content type value
            content = (((contentType.split(";"))[0]).split("/"))[1]
            fileExtension = "" if fileName.find(".") >= 0 else content
            # writing to the body file
            # which will be created if it doesn't exist
            # using 'w' to write string to the file
            bodyFile = open(fileName + "." + fileExtension, 'w')
            bodyFile.write(body.decode("utf-8"))
            # writing to the header file
            # which will be created if it doesn't exist
            headerFile = open("html_header.txt", 'w')
            headerFile.write(header.decode("utf-8"))
    # showing the header file content on the console
    print(header.decode("utf-8"))


# method to create a dictionary for header content from header string
def createHeaderDict(header):
    headerDict = dict()
    headerLines = header.split("\r\n")
    for i in range(1, len(headerLines)):
        keyValue = headerLines[i].split(": ")
        headerDict[keyValue[0]] = keyValue[1]

    return headerDict


# creating function to keep socket open till we receive all data
# or connection timeout(default 3 seconds)
def recvFullResponse(socket, timeout=3.0):
    # using non blocking sockets
    socket.setblocking(0)

    # variables to hold our partial and final completed data
    # received from the server
    allData = list()
    partialData = ''

    # begin counting time for timeout
    startTime = time.time()

    # variable to determine how much data we want to receive
    bytesSize = 1024

    while True:
        # we don't need to wait if we didn't receive any further data
        # than what we already received
        if allData and time.time() - startTime > timeout:
            break
        # wait double timeout if we didn't get any data at all
        # then break with a readable message to the user
        elif time.time() - startTime > timeout * 2:
            return "Time out and No Data Recieved"
        else:
            # try catch block
            # trying to receive data if nothing received we just do
            # another loop till the server responded with some data
            try:
                # receiving data
                partialData = socket.recv(bytesSize)
                # check if the get request result status is 200 OK
                # the bytesSize variable is used to not recheck
                # for each and every next part of the data
                if bytesSize == 1024 and (str(partialData)).find("200 OK") < 0:
                    return ''.join(partialData)
                else:
                    bytesSize = 4096
                    if partialData:
                        # append new data to already received data
                        allData.append(partialData)
                        # for sure reset start time if we get data
                        # to be sure we didn't get timeout before
                        # data receiving completion
                        startTime = time.time()
                    # wait for a while before doing another loop
                    else:
                        time.sleep(0.1)

            except:
                pass

    # use join with empty byte to return data
    # in a one byte sequence, for later extracting header purposes
    return b''.join(allData)


try:
    # create TCP socket
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Socket Creation Failed")

# accepting user inputs from command line
userInput = input("URL: ")
# parsing url using urlparse library
parsedURL = urlparse(userInput)
filePath = parsedURL.path
# creating server address using the server name from
# parseURL.netloc parameter and setting the port to
serverAdd = (parsedURL.netloc, 80)
# creating get request using the path extracted from the given URL
getRequest = "GET " + filePath + " HTTP/1.0\r\nHost: " + parsedURL.netloc + "\r\n\r\n"

try:
    # connecting to the server
    sckt.connect(serverAdd)
except socket.error:
    print("Connection to the server failed")

try:
    # sending request to the server
    sckt.sendall(bytes(getRequest, "UTF-8"))
    # storing received data in a variable
    receivedData = recvFullResponse(sckt)
    # doing the final work
    getHeaderAndBody(receivedData, filePath)
except:
    print("Sending Message Failed")

# closing socket
sckt.close()
