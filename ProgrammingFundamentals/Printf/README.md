_This project has been created as part of the 42 curriculum by maziza_

# 📚 Project : Printf

## 🔍 Description

This project is a C-coded library which aim to reproduce the behaviour of the libc function "_printf_". The reproduced behaviour only concerns some flags (%d, %s or \*p i.e), and the return value of the base function.

## 📁 Content

You'll find here all files names and their purposes/how they work:

- ft_putchar.c : Prints an only character, while increasing the counter of printed elements.

- ft_putstr.c : Prints a string, using ft_putchar.

- ft_putnbr.c : Prints a number in a given base (decimal, hexadecimal), using ft_putchar.

- ft_print_address : Prints the address memory given in the parameter in hexadecimal base.

- ft_strlen : Gives the length of the string in parameter.

- ft_printf : Reads through the string, flags and next parameters, and prints either the 1st parameter or the next ones according to the flag present in the 1st parameter.

- libftprintf.h : Lists all includes needed for the function to work.

## 📜 Instructions

To use this library, one must execute the `make` command, followed by the following flags to compile the latter :

`make all` : Compile all the **.c** files into their corresponding **.o** files, which are then compiled with the **libft.h** header into a **libftprintf.a** archive.

`make clean` : Deletes all the **.o** files from the folder.

`make fclean` : Execute the `make clean` process, but deletes the **libft.a** archive as well.

`make re` : Execute the `make fclean` process, followed by the `make all` one.

## 🌐 Resources

Online websites used to understand the basics of va_list, va_arg and va_end.
