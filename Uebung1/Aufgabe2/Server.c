#include <bits/stdc++.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa.inet.h>
#include <netinet/in.h>

#define PORT 8080

// driver code
int main() {
    int sockfd;
    char buffer[1024];
    const char *hello = "Hello from Server";
    struct sockaddr_in servAddr, cliAddr;

    // creating socket file descriptor
    if((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servAddr, 0, sizeof(servAddr));
    memset(&cliAddr, 0, sizeof(cliAddr));

    // filling server information
    servAddr.sin_family = AF_INET;                 // using IPv4
    servAddr.sin_addr.s_addr = INADDR_ANY;
    servAddr.sin_port = htons(PORT);

    // binding the socket to the server address
    if(bind(sockfd, (const struct sockaddr *) &servAddr, sizeof(servAddr)) <0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    socklen_t len = sizeof(cliAddr);
    int n = recfrom(sockfd, (char *)buffer, 1024, MSG_WAITALL, (struct sockaddr *) &cliAddr, &len);
    buffer[n] = '\0';
    printf("Client: %s \n", buffer);
    
    sendto(sockfd, (const char *)hellom strlen(hello), MSG_CONFIRM, (const struct sockaddr *) &cliAddr, len);
    std::cout<<"Hello message sent."<<std::endl;

    return 0;
}