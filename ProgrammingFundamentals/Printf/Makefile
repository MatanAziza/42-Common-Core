NAME = libftprintf.a

CFLAGS = -Wall -Wextra -Werror

SRC = puts/ft_putnbr.c\
	  puts/ft_print_address.c\
	  puts/ft_putchar.c\
	  puts/ft_putstr.c\
	  ft_printf.c\
	  ft_strlen.c\
	
OBJ = $(SRC:.c=.o)

CCFLAGS = cc -Wall -Wextra -Werror

all:$(NAME)

$(NAME):$(OBJ)
	ar rcs $(NAME) $(OBJ) ft_printf.h

clean:
	rm -rf $(OBJ)

fclean:clean
	rm -rf $(NAME)

re:fclean all


