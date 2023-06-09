import socket
import threading
import sys

if __name__ == '__main__':
    serverAddress = input("Enter server ip: ")
    serverPort = input("Enter server port: ")
    server = (serverAddress, int(serverPort))

    clientInfo = input("Please enter your information: 'name ip port': ")
    clientInfoList = clientInfo.split()
    client_address = clientInfoList[1]
    client_port = int(clientInfoList[2])
    
    # connecting to the server 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # makes the socket reusable
    clientSocket.sendto(bytes("l " + clientInfo, 'utf-8'), server)

    # em server en afrog schecke metem name 
    requestMessage = input("Who do you want to message? (Wait for other person to log in first!)--->")
    clientSocket.sendto(bytes("n " + requestMessage, 'utf-8'), server)
    peer = requestMessage
    
    # gets address information of other client 
    inMessage, addr = clientSocket.recvfrom(1024)
    inMessage = str(inMessage, 'utf-8')
    ip, port = inMessage.split()
    other_client_address = (ip, int(port))
    partner = (ip, port)         
    # print("vom server received: "  + inMessage)           
    
    # connecting to the other client
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.bind((client_address, client_port))

    def send_function(clientSocket):
        while True:
            user_input = input()
            clientSocket.sendto(bytes(user_input, 'utf-8'), other_client_address)

    sendThread = threading.Thread(target=send_function, args=(clientSocket,))
    sendThread.start()


    def recieve_function(clientSocket):
        while True:
            message_from_other_client, address = clientSocket.recvfrom(1024)
            print(peer + ": " + str(message_from_other_client, 'utf-8'))
    
    recieveThread = threading.Thread(target=recieve_function, args=(clientSocket,))
    recieveThread.start()