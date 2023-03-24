#include <stdio.h>
#include <strings.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include<netinet/in.h>
#include<unistd.h>
#include<stdlib.h>

int main(int argc, char const *argv[])
{
    char * input = argv[1];

    char * elementOne = strsep(&input, ":");
    char * elementTwo = strsep(&input, ":");

    printf("%s\n", elementOne);
    printf("%s\n", elementTwo);

    return 0;
}
