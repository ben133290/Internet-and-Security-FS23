#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <pthread.h>
#define PORT 6969

int main(int argc, char const* argv[])
{
    
    char buffer[1024] = { 0 };
    char* hello = "Hello from server";

    /* 
    Creating server socket, 
    server_fd is -1 if failed
    AF_INET means it's IPv4
    SOCK_STREAM means it's a tcp connection :)
    */

    int server_socket;

    if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }



    /*
    Now we have to bind the socket to an ip address
    */

    struct sockaddr_in my_addr; // comes from one of the libraries, don't know which one
    int addrlen = sizeof(my_addr); // length of the address structure because we give the pointer as a param

    bzero(&my_addr, sizeof(my_addr)); // i have no idea wth this does but I found it online hehe
    my_addr.sin_family = AF_INET; // has to match the socket() call
    my_addr.sin_port = htons(PORT); // specify port to listen on
    my_addr.sin_addr.s_addr = htonl(INADDR_ANY); //allow the server to accept a client connection on any interface
    
    // " (struct sockaddr*)&my_addr " is just ugly because it's c, in java this would be " SocketAdress myAddress "
    if (bind(server_socket, (struct sockaddr*)&my_addr, addrlen) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
  
    /*
    Now the server is ready to listen for new connections.
    Only servers need to listen. 
    This does NOT mean that it connects to a new connection, it just listens... 
    the second argument in listen() is int backlog
    = the maximum number of pending connections the kernel should queue for the socket
    */

    if (listen(server_socket, 10) < 0) { 
        perror("listen failed");
        exit(EXIT_FAILURE);
    }

    /*
    Now the server is ready to accept the new connections.
    int accept (int sockfd, struct sockaddr *fromaddr, socklen_t *addrlen)
    */

    int client_socket, valread;

    if ((client_socket = accept(server_socket, (struct sockaddr*)&my_addr, (socklen_t*)&addrlen)) < 0) {
        perror("accept failed");
        exit(EXIT_FAILURE);
    }

    /*
    usage: read (sockfd, buffer, ssize_t N);
    the read() function reads N bytes of input into the memory area indicated by buffer.
    */ 

    valread = read(client_socket, buffer, 1024);
    printf("%s\n", buffer);

    send(client_socket, hello, strlen(hello), 0);
    printf("Hello message sent\n");
    

    /*
    network protocol:

    Log in:
    l:127.0.0.1:4000:name

    get info of another client:
    i:name

    response: 127.0.0.1:4000
    */

    while (strcmp(buffer, "stop") != 0) {

        // clear buffer
        for (int i = 0; i < 1024; i++) {
            buffer[i] = '\0';
        }

        valread = read(client_socket, buffer, 1024);
        // print for debug
        printf("%s\n", buffer);

        if (strcmp(buffer[0], 'l') == 0) {
            

        }
        if (strcmp(buffer))
        sleep(1);
        
    }

    /*
    We have to close the socket after we're done 'cause reasons.
    */
    close(client_socket);
    

    /*
    Also close the server socket.
    */
    shutdown(server_socket, SHUT_RDWR);
    return 0;
    
}