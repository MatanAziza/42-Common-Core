NAME    = codexion
CC      = cc
CFLAGS  = -Wall -Wextra -Werror -pthread -g

SRC     = compile.c debug.c free_mallocs.c main.c parser.c queue.c refactor.c \
          supervisor.c thread.c time_management.c utils.c

OBJDIR  = prefiles
OBJS    = $(SRC:%.c=$(OBJDIR)/%.o)

all: $(NAME) exec

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

$(OBJDIR)/%.o: %.c
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJDIR)

fclean: clean
	rm -rf $(NAME) vgcore.*

re: fclean all

exec: $(NAME)
	clear
	./$(NAME) 4 100 5 3 2 2 5 fifo

val: $(NAME)
	valgrind --leak-check=full ./$(NAME) 4 100 5 3 2 2 5 fifo

.PHONY: all clean fclean re exec val
