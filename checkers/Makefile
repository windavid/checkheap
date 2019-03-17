# universal-makefile
# original here: https://github.com/fedorenchik/universal-makefile.git
c_wildcards := c_*.c 
most_recent_source := $(shell ls -At $(wildcard $(c_wildcards)) | head -1)

.DEFAULT_GOAL := $(basename $(most_recent_source))

CC = gcc

BOOST_LIBS += -lboost_filesystem -lboost_system -lboost_regex \
	      -lboost_date_time -lboost_chrono -lboost_timer -lboost_iostreams \
	      -lboost_thread -lboost_coroutine

CPPFLAGS += -I. -Iinclude -I../include
CFLAGS += -pthread -Wall -Wextra -ggdb3 -O0
CXXFLAGS += -std=c++17 $(CFLAGS)
LDFLAGS += -rdynamic -pthread -L. -Llib -L../lib
LDLIBS += -pthread -lrt -lm $(BOOST_LIBS)

binaries := $(basename $(wildcard $(c_wildcards)))

all: $(binaries)

clean:
	rm -f $(binaries)

help:
	@echo 'make            build most recent source ($(most_recent_source))'
	@echo 'make <prog>     build prog.c'
	@echo 'make all        build all sources'
	@echo 'make clean      remove all binaries'
	@echo 'make help       show this help'

%: %.c
	$(CC) $^ -o $@

.PHONY: all clean help
