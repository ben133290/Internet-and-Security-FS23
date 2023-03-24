import select
import socket
import struct
import sys

MULTICAST_TTL = 2

ip = sys.argv[1]  # ip adresse des servers über commando zeile
port = int(sys.argv[2])  # port über commando zeile
nickname = sys.argv[3]  # eigenen nickname über commando zeile eingeben

# Für Verbindung zum Server
localSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Schicke eine Anfrage für die Chaträume an den Server
localSock.sendto('roomlist'.encode(), (ip, port))

# empfange List von Server und gib sie aus
msg, ipServer = localSock.recvfrom(1024)
print(msg.decode())

# Beende die Verbindung zum Server
localSock.close()

# Angaben zum gewünschten Chatroom über die Console einlesen
ipRoom = input("c~ Please enter the IP of the room you want to join: ")
portRoom = int(input("c~ Please enter the port of the room you want to join: "))

# Neue Sockets für Multicast (Chatraum) er- und einstellen

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
            msg = mSockRec.recv(10240)
            print(msg.decode())
            break

        # wenn Nachricht von eigener Eingabe kommt
        if descriptor is inputDescriptor:
            inp = input()
            msg = nickname + ':' + inp
            mSockSend.sendto(msg.encode(), tuple((ipRoom, portRoom)))

            # Schlüsselwort, um die Unterhaltung und Verbindung abzubrechen
            if inp == 'end':
                print('c~ socket is closing now')
                mSockRec.close()
                mSockSend.close()
            break

