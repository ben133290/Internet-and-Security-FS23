import sys
import socket
import threading
    

server_address = "127.0.0.1"
server_port = 5000

newest_message = ""

list_of_chat_rooms = ['224.1.1.1', '127.0.0.1'] # change depending on what client needs

# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_address, server_port))


while True:

    print("waiting for messages\n")
    data, addr = server_socket.recvfrom(1024)
    message = str(data, 'utf-8')
    print("received message: " + message)

    server_socket.sendto(bytes(str(list_of_chat_rooms), 'utf-8'), addr)
    


