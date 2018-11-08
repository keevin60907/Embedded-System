CC = gcc
INCLUDE = .
LIBS=`pkg-config gstreamer-1.0 --libs`
CFLAGS=`pkg-config gstreamer-1.0 --cflags`


all: gst_stream_client pi-server-raspivid 

pi-server-raspivid: pi-server-raspivid
	$(CC) -I$(INCLUDE) $(CFLAGS) -o pi-server-raspivid pi-server-raspivid.c $(LIBS)

gst_stream_client: gst_stream_client.c
	$(CC) -I$(INCLUDE) $(CFLAGS) -o gst_stream_client gst_stream_client.c $(LIBS)

clean:
	rm -f *.o
	rm -f pi-server-raspivid
	rm -f gst_stream_client
