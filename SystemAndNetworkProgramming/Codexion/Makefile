NAME    = codexion
CC      = cc
CFLAGS  = -Wall -Wextra -Werror -pthread

SRC     = compile.c debug.c free_mallocs.c main.c parser.c queue.c refactor.c \
          steps.c thread.c time_management.c utils.c

OBJDIR  = prefiles
OBJS    = $(SRC:%.c=$(OBJDIR)/%.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

$(OBJDIR)/%.o: %.c
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJDIR)

fclean: clean
	rm -f $(NAME)

re: fclean all

val: $(NAME)
	valgrind --leak-check=full ./$(NAME) 4 1500 500 200 300 5 100 fifo

.PHONY: all clean fclean re val
