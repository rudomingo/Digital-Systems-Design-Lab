# Laboratory Exercise 4 Submission
Student Name 1:

Student Name 2:

## Part 1
Please attach your implementation of the function ```yuyv_to_rgb32``` here.
```c
static void yuyv_to_rgb32 (int width, int height, char *src, long *dst)
{
    unsigned char *s;
    unsigned long *d;
    int l, c, alpha = 0x0;
    int r, g, b, cr, cg, cb, y1, y2;

    l = height;
    s = src;
    d = dst;
    while (l--) {
        c = width >> 1;
        while (c--) {
            y1 = *s++;
            cb = ((*s - 128)*454) >> 8;
            cg = (*s++ - 128) * 88;

            y2 = *s++;
            cr = ((*s - 128)*359) >> 8;
            cg = (cg + (*s++ - 128)*183) >> 8;

            r = y1 + cr;
            b = y1 + cb;
            g = y1 - cg;
            SAT(r);
            SAT(g);
            SAT(b);
            *dst++ = (alpha << 24) | (r << 16) | (g << 8) | b;

            r = y2 + cr;
            b = y2 + cb;
            g = y2 - cg;
            SAT(r);
            SAT(g);
            SAT(b);
            *dst++ = (alpha << 24) | (r << 16) | (g << 8) | b;

        }
    }
}

```

## Part 2
Please attach the ```main``` functions of your udp-send and udp-recv here.
```c
// Attach your implementation of udp-send here
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
  strcpy(buf, message);

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

// Attach your implementation of udp-recv here
int main(int argc, char **argv)
{
	struct sockaddr_in myaddr;	            /* our address */
	struct sockaddr_in remaddr;	            /* remote address */
	socklen_t addrlen = sizeof(remaddr);		/* length of addresses */
	int recvlen;			                      /* # bytes received */
	int fd;				                          /* our socket */
	int msgcnt = 0;			                    /* count # of messages we received */
	unsigned char buf[BUFSIZE];	            /* receive buffer */

	if ((fd=socket(AF_INET, SOCK_DGRAM, 0))==-1) return 0;

	memset((char *)&myaddr, 0, sizeof(myaddr)); 
	myaddr.sin_family = AF_INET; 
	myaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
	myaddr.sin_port = htons(SERVICE_PORT); 
	
	if (bind(fd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) { 
		perror("bind failed"); 
		return 0; 
	}

	/* now loop, receiving data and printing what we received */
	for (;;) {
		printf("waiting on port %d\n", SERVICE_PORT);
    
    /* TODO: receive a message from fd */
    int recvlen = recvfrom(fd, buf, BUFSIZE, 0, (struct sockaddr *)&remaddr, &addrlen);
    /* Check the received message and print out the first character */
		if (recvlen > 0) {
			buf[recvlen] = 0;
      printf("received message: (%d bytes)\n", recvlen);
      printf("entire string: %s\n", buf);
		}
		else
			printf("uh oh - something went wrong!\n");

		sprintf(buf, "ack %d", msgcnt++);
		printf("sending response \"%s\"\n", buf);
		if (sendto(fd, buf, strlen(buf), 0, (struct sockaddr *)&remaddr, addrlen) < 0)
			perror("sendto");
	}
	close(fd);
}

```

## Part 3
Please attach the ```camera``` function in ```./netvideo/camera.c``` and the ```display``` function in ```./netvideo/display.c``` here.
```scala
// Attach your implementation of camera here
static int camera(int fd_v4l)
{
    // Create network client
    struct sockaddr_in myaddr, remaddr;
    int netfd, neti, netslen=sizeof(remaddr);
    char netbuf[NETBUFSIZE]; /* message buffer */

    if ((netfd=socket(AF_INET, SOCK_DGRAM, 0)) == -1)

    /* bind it to all local addresses and pick any port number */
    memset((char *)&myaddr, 0, sizeof(myaddr));
    myaddr.sin_family = AF_INET;
    myaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    myaddr.sin_port = htons(0);

    if (bind(netfd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) {
        perror("bind failed");
        return 0;
    }

    memset((char *) &remaddr, 0, sizeof(remaddr));
    remaddr.sin_family = AF_INET;
    remaddr.sin_port = htons(SERVICE_PORT);
    if (inet_aton(server, &remaddr.sin_addr)==0)
    {
        fprintf(stderr, "inet_aton() failed\n");
        exit(1);
    }

    // Video stream
    struct v4l2_buffer buf;
    struct v4l2_format fmt;

    fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    if (ioctl(fd_v4l, VIDIOC_G_FMT, &fmt) < 0)
    {
        printf("get format failed\n");
        return -1;
    }

    if (start_capturing(fd_v4l) < 0)
    {
        printf("start_capturing failed\n");
        return -1;
    }

    size_t packetsize = NETBUFSIZE - 1;

    for(;;) {
        memset(&buf, 0, sizeof(buf));
        buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory = V4L2_MEMORY_MMAP;
        if (ioctl (fd_v4l, VIDIOC_DQBUF, &buf) < 0) {
            printf("VIDIOC_DQBUF failed.\n");
            break;
        }

        char packetind = 0;
        for(packetind; packetind < NUMPACKFRAME; packetind ++)
        {
          memset(netbuf, packetind, 1);
          memcpy(netbuf+1, (char*)buffers[buf.index].start+(packetsize*packetind), packetsize);
          if (sendto(netfd, netbuf, NETBUFSIZE, 0, (struct sockaddr *)&remaddr, netslen)==-1) {
            perror("sendto");
            exit(1);
          }
        }

        if (ioctl (fd_v4l, VIDIOC_QBUF, &buf) < 0) {
            printf("VIDIOC_QBUF failed\n");
            break;
        }
    }

    if (stop_capturing(fd_v4l) < 0)
    {
        printf("stop_capturing failed\n");
        return -1;
    }

    close(fd_v4l);
    return 0;
}

// Attach your implementation of display here
static int display()
{
    // Create network server
    struct sockaddr_in myaddr;  /* our address */
    struct sockaddr_in remaddr; /* remote address */
    socklen_t addrlen = sizeof(remaddr);        /* length of addresses */
    int recvlen;            /* # bytes received */
    int netfd;             /* our socket */
    unsigned char netbuf[NETBUFSIZE]; /* receive buffer */

    /* create a UDP socket */
    if ((netfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("cannot create socket\n");
        return 0;
    }

    /* bind the socket to any valid IP address and a specific port */
    memset((char *)&myaddr, 0, sizeof(myaddr));
    myaddr.sin_family = AF_INET;
    myaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    myaddr.sin_port = htons(SERVICE_PORT);

    if (bind(netfd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) {
        perror("bind failed");
        return 0;
    }


    // fb
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    long screensize, index;
    int fbfd = 0;
    char *fbp;
    long *bgr_buff;
    char *yuv_buff;

    if ((fbfd = open(g_fb_device, O_RDWR, 0)) < 0)
    {
        printf("Unable to open %s\n", g_fb_device);
        return 0;
    }

    /* Get fixed screen information */
    if (ioctl(fbfd, FBIOGET_FSCREENINFO, &finfo)) {
        printf("Error reading fixed information.\n");
        exit(2);
    }

    /* Get variable screen information */
    if (ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo)) {
        printf("Error reading variable information.\n");
        exit(3);
    }

    /* Figure out the size of the screen in bytes */
    screensize = vinfo.xres * vinfo.yres * vinfo.bits_per_pixel / 8;

    /* Map the device to memory */
    fbp = (char *) mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED,fbfd, 0);
    if ((int)fbp == -1) {
        printf("Error failed to map framebuffer device to memory.\n");
        exit(4);
    }


    bgr_buff = (long *) malloc (sizeof(long) * g_out_width * g_out_height * 4);
    yuv_buff = (char *) malloc (sizeof(char) * g_out_width * g_out_height * 2);
    size_t packetsize = NETBUFSIZE - 1;

    for(;;) {
        char packetiter = 0;
        for (packetiter; packetiter < NUMPACKFRAME; packetiter ++)
        {
	    int recvlen = recvfrom(netfd, netbuf, NETBUFSIZE, 0, (struct sockaddr *)&remaddr, &addrlen);
	    char index = *netbuf;
	    memcpy(yuv_buff + packetsize * index, netbuf + 1, packetsize);  
        }
	yuyv_to_rgb32(g_out_width, g_out_height, yuv_buff, bgr_buff);
        memcpy(fbp, bgr_buff, (vinfo.xres * vinfo.yres * vinfo.bits_per_pixel)/8);
    }

    free(bgr_buff);
    free(yuv_buff);
    munmap(fbp, screensize);
    close(fbfd);
    return 0;
}


```
