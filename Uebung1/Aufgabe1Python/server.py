import socket
import sys
import select

if __name__ == '__main__':
    # setting server IP and port
    serverIP = input("Enter Server IP: ")
    serverPort = input("Enter Server Port: ")
    server = (serverIP, int(serverPort))

    # creating a socket 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(server)   # binding ip to port

    print("waiting for client ... \n")
    serverSocket.listen()
    connection, address = serverSocket.accept()     # accepts new connections
    print("client connected \n")


    socketDescriptor = connection.fileno()
    inputDescriptor = sys.stdin.fileno()

    # while loop using select which recognizes if things are sent or received
    while True:
        readReady, writeReady, exceptionReady = select.select([socketDescriptor, inputDescriptor], [], [])

        # parsing input
        for descriptor in readReady:

            # receiving messages
            if descriptor is socketDescriptor:
                msg = connection.recv(1024)
                print("peer: " + msg.decode())
                break

            # sending input
            if descriptor is inputDescriptor:
                user_input = input()
                msg = user_input
                connection.sendall(msg.encode())

                # typing "end" will stop client
                if user_input == "end":
                    print("socket closing now")
                    connection.close()
                break