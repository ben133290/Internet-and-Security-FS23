import socket
import threading
import struct

if __name__ == '__main__':
    serverPort = 5000
    
    serverAddress = "127.0.0.1"
    server = (serverAddress, int(serverPort))

    clientInfo = input("Press enter to get chatroom list")
    
    # connecting to the server 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # makes the socket reusable
    clientSocket.sendto(bytes(clientInfo, 'utf-8'), server)
    
    # gets address information of other client 
    inMessage, addr = clientSocket.recvfrom(1024)
    inMessage = str(inMessage, 'utf-8')       
    print("vom server received: "  + inMessage)   

    MCAST_GRP = '224.1.1.1' # make changable later
    MCAST_PORT = 5004

    ## UDP MULTICAST PART
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    clientSocket.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    clientSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    MULTICAST_TTL = 2

    def send_function(clientSocket):
        while True:
            user_input = input("enter chat message: ")
            clientSocket.sendto(bytes(user_input, 'utf-8'), (MCAST_GRP, MCAST_PORT))

    sendThread = threading.Thread(target=send_function, args=(clientSocket,))
    sendThread.start()


    def recieve_function(clientSocket):
        while True:
            print(clientSocket.recv(10240))
    
    recieveThread = threading.Thread(target=recieve_function, args=(clientSocket,))
    recieveThread.start()