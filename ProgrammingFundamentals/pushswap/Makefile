# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/19 15:59:07 by jenicola          #+#    #+#              #
#    Updated: 2025/11/21 19:47:37 by jenicola         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# Compiler and flags
CFLAGS :=  -Wextra -Werror -Wall -g -I .

CC := gcc

# Build directory
DIR := build


# # List of source files (all matched wildcards in source directory !)
# SRC := $(wildcard *.c ) 
# easy but not allowed. Therefore :
#
# SRC := handlers/numbers.c  handlers/strings.c  printf.c  utils/signed.c  utils/unsigned.c

SRC := atol_2.c bucket_sort.c main.c optimization_output_cancel.c split.c strings.c \
atol.c disorder.c memory.c optimization_output_combine.c stack_actions.c \
bench_2.c ft_printf.c minmax.c optimization_utils.c stack.c \
bench.c ft_puts.c node.c output.c stack_operations.c \
bubble_sort.c input.c optimization.c radix.c stack_operations_swap.c \
# Now transcripting the sources to .o. Puts them in a build directory
# (needs to be created thanks to the DIR variable)
OBJ := $(patsubst %.c, build/%.o, $(SRC))
# Target
NAME := push_swap

HEADERS := $(wildcard *.h )
# pushswap.h
# could do sth like :
# CFLAGS += -MMD -MP
#-include $(OBJ:.o=.d)




# Default rule
all: $(NAME)

# Rule to build the .a library from all .o
$(NAME): $(OBJ)
		$(CC) $(OBJ) -o $@ -lm

$(DIR):
	mkdir -p build

# Pattern rule to build .o from .c
build/%.o: %.c ${HEADERS} | $(DIR)
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean rules
clean:
	rm -rf $(DIR)

fclean: clean
	rm -f $(NAME)
re: fclean all

.PHONY : clean all fclean re
