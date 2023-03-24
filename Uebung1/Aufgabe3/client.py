import socket
import threading
import struct
import sys

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

    # close the socket to the server
    clientSocket.close()

    # room ip and port
    MCAST_GRP = '224.1.1.1' # make changable later
    MCAST_PORT = 5004

    # Socket für das Senden
    mSockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    mSockSend.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, socket.IPPROTO_UDP)

    # Socket für das Empfangen
    mSockRec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    mSockRec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mSockRec.bind((ipRoom, portRoom))
    mreq = struct.pack('4sl', socket.inet_aton(ipRoom), socket.INADDR_ANY)
    mSockRec.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Jetzt kann das Chatting beginnen
    print('c~ You entered a room. Enter a message to chat:')
    socketDescriptor = mSockRec.fileno()  # descriptor nr für andere Clients
    inputDescriptor = sys.stdin.fileno()  # descriptor nr für die eigene Eingabe

while True:
    readReady, writeReady, exceptionReady = select.select([socketDescriptor, inputDescriptor], [], [])

    # Behandlung aller eingehenden Inhalte (über Socket-Verbindung oder Tastatur)
    for descriptor in readReady:

        # wenn Nachricht von anderem Client kommt
        if descriptor is socketDescriptor:
            msg = clientSocket.recv(10240)
            print(msg.decode())
            break

        # wenn Nachricht von eigener Eingabe kommt
        if descriptor is inputDescriptor:
            inp = input()
            msg = inp
            clientSocket.sendto(msg.encode(), tuple((ipRoom, portRoom)))

            # Schlüsselwort, um die Unterhaltung und Verbindung abzubrechen
            if inp == 'end':
                print('c~ socket is closing now')
                clientSocket.close()
                mSockSend.close()
            break