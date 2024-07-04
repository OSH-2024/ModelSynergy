CC = gcc
CFLAGS = $(shell pkg-config --cflags glib-2.0) -Wall -g
LIBS = $(shell pkg-config --libs glib-2.0)

all: watch trans

watch: inotify.c ../task_queue/send.c
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

trans: trans.c ../task_queue/receive.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f watch trans