// Client side C/C++ program to demonstrate Socket
// programming
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#define PORT 6969
  
int main(int argc, char const* argv[])
{
    
    /*
    check if supplied arguments are correct 
    */

    if (argc != 2) {
        printf("usage: ./server <ip>\n");
        printf("number of arguments supplied: %d\n", argc);
        return 1;
    }

    const char* server_ip = argv[1];
    printf("Connecting to server at ip: %s\n", server_ip);

    int client_fd;
    
    char* hello = "Hello from client";
    char buffer[1024] = { 0 };

    /*
    creates the client socket
    server_fd is -1 if failed
    AF_INET means it's IPv4
    SOCK_STREAM means it's a tcp connection :)
    */

    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    /*
    Set socket address parameters to match socket defined above
    */
  
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
  
    // Convert IPv4 and IPv6 addresses from text to binary
    // form
    if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    /*
    Here we connect to the server
    */
    
    int valread;
    int status;
  
    if ((status = connect(client_fd, (struct sockaddr*) &serv_addr, sizeof(serv_addr))) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }
    send(client_fd, hello, strlen(hello), 0);
    printf("Hello message sent\n");
    valread = read(client_fd, buffer, 1024);
    printf("%s\n", buffer);
  
    // closing the connected socket
    close(client_fd);
    return 0;
}