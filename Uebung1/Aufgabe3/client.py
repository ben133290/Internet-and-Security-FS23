import socket
import threading
import struct
import sys
import select

if __name__ == '__main__':
    
    serverAddress = input("Enter server address: ")
    serverPort = input("Enter server port: ")
    server = (serverAddress, int(serverPort))

    clientInfo = input("Press enter to get chatroom list")
    
    # connecting to the server 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # makes the socket reusable
    clientSocket.sendto(bytes(clientInfo, 'utf-8'), server)
    
    # gets address information of other client 
    inMessage, addr = clientSocket.recvfrom(1024)
    inMessage = str(inMessage, 'utf-8')
    print("List of rooms: "  + inMessage)

    # close the socket to the server
    clientSocket.close()

    # lets user set room ip and port
    MCAST_GRP = input("Enter the multicast ip of the room you want to enter: ")
    MCAST_PORT = int(input("Enter the port number of the room: "))

    # create socket for sending
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sendSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, socket.IPPROTO_UDP)

    # Socket für recieving messages from other clients
    recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recvSocket.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    recvSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Entered room
    print('You entered a room. Enter a message to chat:')
    socketDescriptor = recvSocket.fileno()  # descriptor nr for other Clients
    inputDescriptor = sys.stdin.fileno()  # descriptor nr for user input

while True:
    readReady, writeReady, exceptionReady = select.select([socketDescriptor, inputDescriptor], [], [])

    # parse inputs
    for descriptor in readReady:

        # recieve message from group
        if descriptor is socketDescriptor:
            msg = recvSocket.recv(10240)
            print(msg.decode())
            break

        # send user input to group
        if descriptor is inputDescriptor:
            user_input = input()
            msg = user_input
            sendSocket.sendto(msg.encode(), tuple((MCAST_GRP, MCAST_PORT)))

            # user can type end to stop client
            if user_input == 'end':
                print('socket closing now')
                clientSocket.close()
                sendSocket.close()
            break