#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <pthread.h>
#define PORT 6969

void *sendThreadFun(void *vargp) {

    int client_socket = *(int *)vargp;

    // read from system in
    char message[1024];

    while (strcmp(message,"stop") != 0)
    {
        // clear buffer
        for (int i = 0; i < 1024; i++) {
            message[i] = '\0';
        }

        // Get and save the text
        scanf("%[^\n]", message);
        send(client_socket, message, strlen(message), 0);
        sleep(1);
    }
        
    return NULL;
}
  
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

    int client_socket;
    
    char* hello = "client has connected";
    char buffer[1024] = { 0 };

    /*
    creates the client socket
    server_fd is -1 if failed
    AF_INET means it's IPv4
    SOCK_STREAM means it's a tcp connection :)
    */

    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
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
  
    if ((status = connect(client_socket, (struct sockaddr*) &serv_addr, sizeof(serv_addr))) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }

    send(client_socket, hello, strlen(hello), 0);
    printf("Hello message sent\n");
    valread = read(client_socket, buffer, 1024);
    printf("%s\n", buffer);

    //TODO: Start a thread, that listens for user input on the console an then calls send()
    pthread_t sendThread;
    pthread_create(&sendThread, NULL, sendThreadFun, &client_socket);
    //pthread_join(sendThread, NULL);

    //TODO: make a while loop where read() is called, and the recieved message is printed to the console, don't forget to clear buffer
    while (strcmp(buffer, "stop") != 0) {

        // clear buffer
        for (int i = 0; i < 1024; i++) {
            buffer[i] = '\0';
        }

        valread = read(client_socket, buffer, 1024);
        printf("peer: %s\n", buffer);
        sleep(1);

    }
  
    // closing the connected socket
    close(client_socket);
    return 0;
}