CC = gcc
CFLAGS = $(shell pkg-config --cflags glib-2.0) -Wall -g
LIBS = $(shell pkg-config --libs glib-2.0)

all: test

test: inotify.c getxattr.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

clean:
	rm -f test