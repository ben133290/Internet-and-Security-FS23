import socket
import sys

port = int(sys.argv[1])  # port über commando zeile

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", port))  # bindet Socket mit Port von Kommandozeile

# String mit den angaben zu den möglichen Chaträumen
roomList = "Available Chatrooms:\n\nJam On Exclusive Yacht:\nIP: 224.0.0.1 Port: 8091\n\nEat Sweets To Have Excellent Recovery:\nIP: 224.0.0.2 Port: 8092\n\nYoga And Slow Meditation In Neverland:\nIP: " \
           "224.0.0.3 Port: 8093 \n"

print("ready on port:", port)

while True:

    # empfange Nachrichten von Clients
    message, client = sock.recvfrom(1024)

    # wenn die empfangene Nachricht 'roomlist' lautet schickt der Server die entsprechenden Infos.
    # andere eingehende Nachrichten (sollte nicht möglich sein) werden ignoriert.
    if message.decode().startswith('roomlist'):
        sock.sendto(roomList.encode(), client)
        print('new client connected')
