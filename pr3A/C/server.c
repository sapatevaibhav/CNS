#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#define PORT 5561
#define BUF_SIZE 2000
#define RESPONSE_SIZE 100
#define CLADDR_LEN 100
int main() {
    struct sockaddr_in addr, cl_addr;
    int sockfd, len, ret, newsockfd;
    char buffer[BUF_SIZE];
    pid_t childpid;
    char clientAddr[CLADDR_LEN];
    int num, sum;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        printf("Error creating socket!\n");
        exit(1);
    }
    printf("Socket created...\n");
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);
    ret = bind(sockfd, (struct sockaddr *) &addr, sizeof(addr));
    if (ret < 0) {
        printf("Error binding!\n");
        exit(1);
    } else {
        printf("Binding done...\n");
    }
    printf("Waiting for a connection...@ port no : %d\n", PORT);
    listen(sockfd, 5);
    for (;;) { // Infinite loop for accepting connections
        len = sizeof(struct sockaddr_in);
        newsockfd = accept(sockfd, (struct sockaddr *)&cl_addr, (socklen_t *)&len);
        if (newsockfd < 0) {
            printf("Error accepting connection!\n");
            exit(1);
        }
        printf("Connection accepted from %s:%d\n", inet_ntoa(cl_addr.sin_addr), ntohs(cl_addr.sin_port));
        if ((childpid = fork()) == 0) { // Creating a child process
            close(sockfd); // Stop listening for new connections by the main process
            for (;;) { // Infinite loop for communication with client
                memset(buffer, 0, BUF_SIZE);
                ret = recv(newsockfd, buffer, BUF_SIZE, 0);
                if (ret < 0) {
                    printf("Error receiving data!\n");
                    exit(1);
                }
                // Calculate the sum of digits
                num = atoi(buffer);
                sum = 0;
                while (num > 0) {
                    sum += num % 10;
                    num /= 10;
                }
                // Construct the response message
                char response[RESPONSE_SIZE];
                snprintf(response, RESPONSE_SIZE, "%d = sum of digits = %d", atoi(buffer), sum);
                // Send the response message back to the client
                ret = send(newsockfd, response, strlen(response), 0);
                if (ret < 0) {
                    printf("Error sending data!\n");
                    exit(1);
                }
                printf("Sent data to %s:%d: %s\n", inet_ntoa(cl_addr.sin_addr), ntohs(cl_addr.sin_port), response);
            }
        }
        close(newsockfd);
    }
    return 0;
}
