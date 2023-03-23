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
    printf("Enter l:name:ip:port to log in");
    char message[1024];
    scanf("%[^\n]", message);





    // Connect to Server
    int sockfd, n;
    struct sockaddr_in servaddr;
      
    // clear servaddr
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);
    servaddr.sin_family = AF_INET;
      
    // create datagram socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
      
    // connect to server
    if(connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
    {
        printf("\n Error : Connect Failed \n");
        exit(0);
    }




  
    // send l:name:ip:port to server
    sendto(sockfd, message, MAXLINE, 0, (struct sockaddr*)NULL, sizeof(servaddr));


    // read client input (name)
    char nameOfOtherClient[40];
    char request[] = "i:";
    scanf("%[^\n]", nameOfOtherClient);
    strcat(request, nameOfOtherClient);

    // send request to server
    sendto(sockfd, request, MAXLINE, 0, (struct sockaddr*)NULL, sizeof(servaddr));

    // read server message
    char buffer[100];
    recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr*)NULL, NULL);
    puts(buffer);

    // start udp connection
    

    // close the descriptor
    close(sockfd);
}