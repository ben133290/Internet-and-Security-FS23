// server program for udp connection
#include <stdio.h>
#include <strings.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include<netinet/in.h>
#define PORT 5000
#define MAXLINE 1000

typedef struct name_ipport
{
    char * name;
    char * ipport;
} clientInfo;
  
// Driver code
int main()
{   

    clientInfo data[10];

    clientInfo info;
    info.name = "ben";
    info.ipport = "127.0.0.1:4000";

    data[1] = info;


    char buffer[100];
    char * message = "Test message";
    int listenfd, len;
    struct sockaddr_in servaddr, cliaddr;
    bzero(&servaddr, sizeof(servaddr));
  
    // Create a UDP Socket
    listenfd = socket(AF_INET, SOCK_DGRAM, 0);        
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);
    servaddr.sin_family = AF_INET; 
   
    // bind server address to socket descriptor
    //bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
       
    //receive the datagram
    int i = 0;

    while (1) {

        // recieve message
        recvfrom(listenfd, buffer, sizeof(buffer), 0, (struct sockaddr*)&servaddr, sizeof(servaddr));

        //if message log in message then save data
        char * command_type = strsep(buffer, " ");
        char * parameter_one = strsep(buffer, " ");
        char * parameter_two = strsep(buffer, " ");

        if (strcmp(command_type, "l") == 0) {
            strcpy(data[i].name, parameter_one);
            strcpy(data[i].ipport, parameter_two);
            i++;
        }

        //if message get info message the giva data
        if (strcmp(command_type, "n") == 0) {
            sendto(listenfd, message, MAXLINE, 0, (struct sockaddr*)&cliaddr, sizeof(cliaddr));
        }

        buffer[0] = '\0'; // clear buffer

    }

    len = sizeof(cliaddr);
    int n = recvfrom(listenfd, buffer, sizeof(buffer),
            0, (struct sockaddr*)&cliaddr,&len); //receive message from server
    buffer[n] = '\0';
    puts(buffer);
           
    // send the response
    sendto(listenfd, message, MAXLINE, 0,
          (struct sockaddr*)&cliaddr, sizeof(cliaddr));
}