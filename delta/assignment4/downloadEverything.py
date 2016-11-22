import socket
from urllib.parse import urlparse
import re

# importing another python file
# this syntax it is used in order to avoid
# the problems caused by the hyphen in the name
taskOne = __import__("http-client")

def getUrls(fileName):
    # opening the file from which we want to get
    # the urls for the images
    file = open(fileName, 'r')
    fileContent = file.read()
    # find all the image tags in order to get the correct urls
    urls = re.findall('<img [^>]*src=\"([^\"]+)', fileContent)
    prsdURL = urlparse(inputUrl)
    # looping over the urls
    # if the first character is /
    # then this is a relative path
    # and we have to make it absolute
    for url in urls:
        if url[0] == '/':
            urls[urls.index(url)] = prsdURL.scheme + "://" + prsdURL.netloc + url
    return urls


# accepting user inputs from command line
inputUrl = input("URL: ")
localFileName = input("File Name: ")
imagesUrls = getUrls(localFileName)
# printing out the urls
print(imagesUrls)
for imgUrl in imagesUrls:

    try:
        # create TCP socket
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("Socket Creation Failed")

    # parsing url using urlparse library
    parseURL = urlparse(imgUrl)
    flPath = parseURL.path
    # creating server address using the server name from
    # parseURL.netloc parameter and setting the port to
    serverAdd = (parseURL.netloc, 80)
    # creating get request using the path extracted from the given URL
    getRequest = "GET " + flPath + " HTTP/1.0\r\nHost: " + parseURL.netloc + "\r\n\r\n"

    try:
        # connecting to the server
        sckt.connect(serverAdd)
    except socket.error:
        print("Connection to the server failed")

    try:
        # sending request to the server
        sckt.sendall(bytes(getRequest, "UTF-8"))
        # using the methods from the first task in order to download the images
        taskOne.getHeaderAndBody(taskOne.recvFullResponse(sckt), flPath)
    except:
        print("Sending Message Failed")

    sckt.close()