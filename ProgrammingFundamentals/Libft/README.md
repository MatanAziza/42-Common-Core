_This project has been created as part of the 42 curriculum by maziza_

# 📚 Project : Libft

## 🔍 Description

This project is a C-coded library consisting of several utilitaries functions, some already existing (such as atoi, calloc or memset), while some are made up for specific tasks (such as ft_split, ft_itoa or ft_strmapi).

## 📁 Content

You'll find here all functions's names and their purposes/how they work:

- ft_isalpha.c : Returns a positive value if the parameter is an alphabetical character, and zero if not.

- ft_isdigit.c : Returns a positive value if the parameter is a numeric character, and zero if not.

- ft_isalnum.c : Returns a positive value if the parameter is an alphanumeric character, and zero if not.

- ft_isascii.c : Returns a positive value if the parameter is part of the ASCII table, and zero if not.

- ft_isprint.c : Returns a positive value if the parameter is a printable character, and zero if not.

- ft_strlen.c : Return the length of the string parameter.

- ft_memset.c : Set the memory area designated by its address to a certain value.

- ft_bzero.c : Set the memory area designated by its address to zero.

- ft_memcpy.c : Copy a memory area from a source to a destination, with no overlap from both the source and the destination.

- ft_memmove.c : Copy a memory area from a source to a destination when they are overlapping.

- ft_strlcpy.c : Copy a string from its source to a destination, ensuring the final length `l` contains both the source and the `\0` character.

- ft_strlcat.c : Concatenate a string from its source to a destination, ensuring the final length `l` contains both the source, the destination's string and the `\0` character.

- ft_toupper.c : Set the character to its uppercase version if possible.

- ft_tolower.c : Set the character to its lowercase version if possible.

- ft_strchr.c : Locate the first occurrence of a character in a string.

- ft_strrchr.c : Locate the last occurrence of a character in a string.

- ft_strncmp.c : Compare two strings up to `n` characters and return the difference between the first differing characters.

- ft_memchr.c : Search for the first occurrence of a byte in a memory area.

- ft_memcmp.c : Compare two memory areas up to `n` bytes and return the difference between the first differing bytes.

- ft_strnstr.c : Locate a substring within a string, searching up to `n` characters.

- ft_atoi.c : Convert a string to an integer.

- ft_calloc.c : Allocate memory for an array and initialize it to zero.

- ft_strdup.c : Duplicate a string by allocating sufficient memory and copying its content.

- ft_substr.c : Create a substring from a string, starting at a given index and for a given length.

- ft_strjoin.c : Concatenate two strings into a newly allocated one.

- ft_strtrim.c : Remove all occurrences of a set of characters from the beginning and the end of a string.

- ft_split.c : Split a string into an array of substrings based on a delimiter character.

- ft_itoa.c : Convert an integer to a string.

- ft_strmapi.c : Apply a function to each character of a string and create a new string with the results.

- ft_striteri.c : Apply a function to each character of a string, modifying it directly.

- ft_putchar_fd.c : Write a single character to the specified file descriptor.

- ft_putstr_fd.c : Write a string to the specified file descriptor.

- ft_putendl_fd.c : Write a string followed by a newline to the specified file descriptor.

- ft_putnbr_fd.c : Write an integer as characters to the specified file descriptor.

- ft_lstnew.c : Create a new list element with a given content.

- ft_lstadd_front.c : Add a new element at the beginning of a list.

- ft_lstsize.c : Count the number of elements in a list.

- ft_lst_last.c : Return the last element of a list.

- ft_lstadd_back.c : Add a new element at the end of a list.

- ft_delone.c : Delete a single element from a list using a specified delete function.

- ft_lstclear.c : Delete and free all elements of a list using a specified delete function.

- ft_lstiter.c : Apply a function to each element of a list.

- ft_lstmap.c : Apply a function to each element of a list, creating a new list from the results.

## 📜 Instructions

To use this library, one must execute the `make` command, followed by the following flags to compile the latter :

`make all` : Compile all the **.c** files into their corresponding **.o** files, which are then compiled with the **libft.h** header into a **libft.a** archive.

`make clean` : Deletes all the **.o** files from the folder.

`make fclean` : Execute the `make clean` process, but deletes the **libft.a** archive as well.

`make re` : Execute the `make fclean` process, followed by the `make all` one.

## 🌐 Resources

[⚙️ LibftTester](https://github.com/Tripouille/libftTester)

[🦈 Christian Aucane](https://github.com/christian-aucane)

AI was used to debug my code after many solo attempts, and to understand some notions not mastered before they were mentionned in the pdf.
