CC = gcc
INCLUDE = .
LIBS=`pkg-config gstreamer-1.0 --libs`
CFLAGS=`pkg-config gstreamer-1.0 --cflags`


all: gst_hello gst_stream_server gst_stream_client 

gst_hello: gst_hello.c
	$(CC) -I$(INCLUDE) $(CFLAGS) -o gst_hello gst_hello.c $(LIBS)

gst_stream_server: gst_stream_server.c
	$(CC) -I$(INCLUDE) $(CFLAGS) -o gst_stream_server gst_stream_server.c $(LIBS)

gst_stream_client: gst_stream_client.c
	$(CC) -I$(INCLUDE) $(CFLAGS) -o gst_stream_client gst_stream_client.c $(LIBS)

clean:
	rm -f *.o
	rm -f gst_hello
	rm -f gst_stream_server
	rm -f gst_stream_client
