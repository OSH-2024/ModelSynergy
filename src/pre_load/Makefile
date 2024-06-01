CC = gcc
CFLAGS = $(shell pkg-config --cflags glib-2.0)
LIBS = $(shell pkg-config --libs glib-2.0)

all: test

test: inotify.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

clean:
	rm -f test