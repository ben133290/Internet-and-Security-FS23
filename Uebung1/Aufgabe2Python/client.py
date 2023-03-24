import socket
import threading
import sys

if __name__ == '__main__':
    serverPort = 5000
    serverAddress = "127.0.0.1"
    server = (serverAddress, int(serverPort))

    clientInfo = input("Please enter: 'name ip port'")
    
    # connecting to the server 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # makes the socket reusable
    clientSocket.sendto("l " + clientInfo, server)

    # em server en afrog schecke metem name 
    requestMessage = input("Who do you want to message?")
    clientSocket.sendto("n " + requestMessage, server)
    
    # gets address information of other client 
    inMessage = clientSocket.recvfrom(1024)
    ip, port = inMessage.split()
    partner = (ip, port)         
    print("vom server received: "  + inMessage)           
    
    # connecting to the other client
    #clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # receive messages
    #while True:
     #   inMessage = clientSocket.recvfrom()

    # send messages