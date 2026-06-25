all:
	cc -Wall -Wextra -Werror -pthread *.c -o codexion;
	clear;
run:
	./codexion 1 1 1 1 1 1 1 fifo
val:
	valgrind --leak-check=full ./codexion 4 2 3 4 5 6 7 fifo
