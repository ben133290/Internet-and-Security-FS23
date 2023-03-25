import socket
import select
import sys

if __name__ == '__main__':
    # setting server IP and port
    serverIP = input("Enter Server IP: ")
    serverPort = input("Enter Server Port: ")
    server = (serverIP, int(serverPort))

    # creating a socket and connecting to the server 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(server)
    print("connected to server \n")
    clientSocket.sendall("test vom client".encode())

    socketDescriptor = clientSocket.fileno()
    inputDescriptor = sys.stdin.fileno()

    while True:
        readReady, writeReady, exceptionReady = select.select([socketDescriptor, inputDescriptor], [], [])

        # parsing input
        for descriptor in readReady:

            # receiving messages
            if descriptor is socketDescriptor:
                msg = clientSocket.recv(10240)
                print("peer: " + msg.decode())
                break

            # sending input
            if descriptor is inputDescriptor:
                user_input = input()
                msg = user_input
                clientSocket.sendall(msg.encode())

                # typing "end" will stop client
                if user_input == "end":
                    print("socket closing now")
                    clientSocket.close()
                break
