// udp client driver program
#include <stdio.h>
#include <strings.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include<netinet/in.h>
#include<unistd.h>
#include<stdlib.h>
  
#define PORT 5000
#define MAXLINE 1000
  
// Driver code
int main()
{   

    // initialize values
    printf("Enter l name ip:port to log in\n");
    char message[1024];
    if (scanf("%[^\n]", message) < 0) { printf("couldn't scan\n"); }
    printf("%s\n", message);


    // Connect to Server
    int server_socket;
    struct sockaddr_in servaddr;
      
    // clear servaddr
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);
    servaddr.sin_family = AF_INET;
      
    // create datagram socket
    server_socket = socket(AF_INET, SOCK_DGRAM, 0);
    printf("Created server socket\n");

    // send l:name:ip:port to server
    if (sendto(server_socket, message, (strlen(message) + 1), 0, (struct sockaddr*) &servaddr, sizeof(servaddr)) < 0) { 
        printf("Couldn't send log in!\n");
    }

    // read client input (name)
    char requestMessage[40];
    printf("Write i name");
    scanf("%[^\n]", requestMessage);

    // send request to server
    if (sendto(server_socket, requestMessage, (strlen(requestMessage) + 1), 0, (struct sockaddr*) &servaddr, sizeof(servaddr)) < 0) {
        printf("Couldn't request ip and port of other user\n"); 
    }

    // read server message
    char buffer[100];
    recvfrom(server_socket, buffer, sizeof(buffer), 0, (struct sockaddr*)NULL, NULL);
    puts(buffer);

    // read out ip and and port
    char * ip_address = strsep(buffer, ':');
    char * port = strsep(buffer, ':');


    // start udp connection
    

    // close the descriptor
    close(server_socket);
}