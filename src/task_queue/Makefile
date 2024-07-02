CC = gcc
CFLAGS = -Wall -g

SOURCES = task_queue.c send.c receive.c test.c
TARGET = test

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES) -o $(TARGET)

clean:
	rm -f $(TARGET)