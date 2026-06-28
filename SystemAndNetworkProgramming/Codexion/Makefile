all:
	cc -Wall -Wextra -Werror -pthread *.c -o codexion;
	clear;
run:
	./codexion 1 1 1 1 1 1 1 fifo
val:
	valgrind --leak-check=full ./codexion 4 1500 500 200 300 5 100 fifo
