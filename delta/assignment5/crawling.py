# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:26:07 2016

@author: Omar K. Aly
"""
"""
Importing libraries section
"""
import socket
from urllib.parse import urlparse
from urllib.parse import urljoin
import time
import re
import queue
import os
import csv

"""
Defining class section
"""
class crawler:
    def extractHostAndPath(url):
        result = list()
        # parsing url using urlparse library
        parsedURL = urlparse(url)
        result.append(parsedURL.path)
        result.append(parsedURL.netloc)
        return result
    def doCrawel(url):
        urlQueue = queue.Queue()
        urlQueue.put(url)
        counter = 1
        badUrlsCounter = 0
        dictOfCrawlableLinks = {url:""}
        while not urlQueue.empty():
            try:
                # create TCP socket
                sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except:
                print("Socket Creation Failed")
            
            underProcessingUrl = urlQueue.get()
            if counter % 500 == 0:
                print("Currently processing url: " + underProcessingUrl)
                
            hostAndPath = crawler.extractHostAndPath(underProcessingUrl)
            host = hostAndPath[1]
            filePath = hostAndPath[0]
            # creating server address using the server name from
            # parseURL.netloc parameter and setting the port to
            serverAdd = (host, 80)
            # creating get request using the path extracted from the given URL
            getRequest = "GET " + filePath + " HTTP/1.0\r\nHost: " + host + "\r\n\r\n"
            try:
                # connecting to the server
                sckt.connect(serverAdd)
            except socket.error:
                print("Connection to the server failed")
                badUrlsCounter += 1
                if dictOfCrawlableLinks[underProcessingUrl]:
                    dictOfCrawlableLinks[underProcessingUrl] += "\nBad URL"
            try:
                # sending request to the server
                sckt.sendall(bytes(getRequest, "UTF-8"))
                # storing received data in a variable
                extractedHtml = crawler.recvFullResponse(sckt)
                extractedBody = crawler.getHeaderAndBody(extractedHtml, filePath)
                if extractedBody == -1:
                    badUrlsCounter += 1
                    if dictOfCrawlableLinks[underProcessingUrl]:
                        dictOfCrawlableLinks[underProcessingUrl] += "\nBad URL"
                    pass
                else:
                    links = crawler.getAllUrls(extractedBody)
                    fullLinks = crawler.absLinkToFullLinks(links, underProcessingUrl)
                    dictOfMarkedLinks = crawler.markExternalLinks(fullLinks, host)
                    for link in dictOfMarkedLinks:
                        if not (link in dictOfCrawlableLinks):
                            dictOfCrawlableLinks[link] = dictOfMarkedLinks[link]
                    for crawlableLink in dictOfCrawlableLinks:
                        if dictOfCrawlableLinks[crawlableLink] == "":
                            urlQueue.put(crawlableLink)
                            dictOfCrawlableLinks[crawlableLink] = "enqueued"
                counter +=1
                if dictOfCrawlableLinks[underProcessingUrl]:
                    dictOfCrawlableLinks[underProcessingUrl] += "\nSuccessfully processed URL"
            except:
                print("Sending Message Failed")
                badUrlsCounter += 1
                if dictOfCrawlableLinks[underProcessingUrl]:
                    dictOfCrawlableLinks[underProcessingUrl] += "\nBad URL"
            # closing socket
            sckt.close()
            
            if counter % 500 == 0:
                print("Number of successfully processed URLs till now: "+ str(counter))
                print("Number of bad URLs till now: "+ str(badUrlsCounter))
                print("Current URLs Queue length: "+ str(urlQueue.qsize()))
            
            logFile = open("downloadedPages/logfile.txt", "a")
            logLine = "Number of successfully processed URLs till now: "+ str(counter) + "\r"
            logLine += "Number of bad URLs till now: "+ str(badUrlsCounter) + "\r"
            logLine += "Current URLs Queue length: "+ str(urlQueue.qsize()) + "\r\n"
            logFile.write(logLine)
            
        with open('downloadedPages/dict.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in dictOfCrawlableLinks.items():
                writer.writerow([key, value])
        
    def markExternalLinks(listOfLinks, mainHost):
        linksDictionary = {listOfLinks[i]: "" for i in range(0, len(listOfLinks))}
        for link in linksDictionary:
            if urlparse(link).netloc != mainHost:
                linksDictionary[link] = "External Link"
                    
        return linksDictionary

    def absLinkToFullLinks(dictOfLinks, mainUrl):
        for i in range(0, len(dictOfLinks)):
            if dictOfLinks[i][0:4] != "http":
                newLink = urljoin(mainUrl, dictOfLinks[i])
                dictOfLinks[i] = newLink
        return dictOfLinks
        
    def getAllUrls(htmlPage):
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', str(htmlPage))
        return urls
        
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
      
    # method to create a dictionary for header content from header string
    def createHeaderDict(header):
        headerDict = dict()
        headerLines = header.split("\r\n")
        for i in range(1, len(headerLines)):
            keyValue = headerLines[i].split(": ")
            headerDict[keyValue[0]] = keyValue[1]
        return headerDict
    # function to separate header from body & print header to console
    # also save body in the appropriate file format according to the
    # content type value of the header
    def getHeaderAndBody(receivedData, fPath):
        if (str(receivedData)).find("200 OK") >= 0:
            try:
                
                # find the starting part of body
                startOfBody = receivedData.find(b"\r\n\r\n")
                # creating the header part
                header = receivedData[:startOfBody]
                # creating the body part
                # the constant 4 is just to escape the \r\n\r\n characters
                body = receivedData[(startOfBody + 4):]
                # creating the header dictionary
                # to know the content type
                headerDictionary = crawler.createHeaderDict(header.decode("utf-8"))
                # extracting the content type of the body
                contentType = headerDictionary["Content-Type"]
                # getting the image name by splitting on the url path
                splittedPath = fPath.split("/")
                fileName = splittedPath[-1]
                directoryPath = '/'.join(splittedPath[0:-1])
                # if the HTTP status is 200 OK we process header & body
                # else we just print out the header
                if not os.path.exists("downloadedPages"):
                    os.makedirs("downloadedPages")
                if not os.path.exists("downloadedPages"+directoryPath):
                    os.makedirs("downloadedPages"+directoryPath)
                #if the file name doesn't have extension we add it
                #using the content type value
                content = (((contentType.split(";"))[0]).split("/"))[1]
                fileExtension = "" if fileName.find(".") >= 0 else content
                # writing to the body file
                # which will be created if it doesn't exist
                # using 'w' to write string to the file
                bodyFile = open("downloadedPages"+directoryPath+"/"+fileName +"."+ fileExtension, 'wb')
                bodyFile.write(body)
                return body
            except:
                return -1
        else:
            return -1
          
"""
Main Section
"""
startTime = time.time()
crawler.doCrawel("http://141.26.208.82/articles/g/e/r/Germany.html")
endTime = time.time()

totalTime = endTime - startTime
print("Crawling time: " + str(totalTime))