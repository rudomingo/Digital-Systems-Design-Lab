#include "port.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define BUFSIZE 61441 /* This would need 30 packets to fill a frame */
#define SERVICE_PORT 21234

int main(void)
{
	struct sockaddr_in myaddr, remaddr;
	int fd, i, slen=sizeof(remaddr);
	char buf[BUFSIZE];	/* message buffer */
	int recvlen;		/* # bytes in acknowledgement message */

  // Create UDP socket 
  if ((fd=socket(AF_INET, SOCK_DGRAM, 0))==-1) return 0;

  // Bind the socket to all local addresses and pick any port number 
  memset((char*)&myaddr, 0, sizeof(myaddr));
  myaddr.sin_family = AF_INET;
  myaddr.sin_addr.s_addr = htonl(INADDR_ANY);
  myaddr.sin_port = htons(0);

  if (bind(fd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) { 
    perror("bind failed");
    return 0;
  }

  // Set message buffer
  char *message = "Thirsty Thursday.";

  // Copy the message to the message buffer, buf
  memcpy(message, buf, sizeof(message));

	// Now define remaddr, the address to whom we want to send messages. For convenience, the host address is expressed as a numeric IP address. We will convert this IP address to a binary format via inet_aton 
  memset((char *) &remaddr, 0, sizeof(remaddr));
  remaddr.sin_family = AF_INET;
  remaddr.sin_port = htons(SERVICE_PORT);
  if (inet_aton(server, &remaddr.sin_addr)==0) {
    fprintf(stderr, "inet_aton() failed\n");
    exit(1);
  }

	// Send the message
  if (sendto(fd, buf, strlen(buf), 0, (struct sockaddr *)&remaddr, slen)==-1) {
    perror("sendto");
    exit(1);
  } 

  // Close fd
	close(fd);
	return 0;
}
