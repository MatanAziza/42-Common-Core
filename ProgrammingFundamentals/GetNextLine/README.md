_This project has been created as part of the 42 curriculum by maziza_

# 📚 Project : Get Next Line

## 🔍 Description

The "Get Next Line" Project is a C-coded projects that allows the user to return the next line of a text document. To do so, the function uses the "read" function in a buffer, and join them as long as there'sno new line character. Whenever that happens (or if the file ends), the read line is returned, while the remaining string is stored in a static buffer, waiting for the function GNL to be called once more, in which case the stored string is sent to the read buffer instead of a read being performed.
If the read fails, the stored string is returned, ending the process instantly.

## 📁 Content

You'll find here all files names and their purposes/how they work:

### **get_next_line_utils.c** functions content :

- ft_strdup : Duplicates a string in a malloced string, which is then returned.

- ft_strchr : A custom version of the _strchr_ function which returns the looked after character's index, or -1 if not found.

- ft_strjoin : A custom version of _strjoin_ which joins 2 strings into a malloced string, which is then returned after freeing the strings used to create the returned one.

- ft_substr : A custom version of _substr_ which returned a malloced string containing a smaller part of a string. The new string is returned after freeing the original one.

- ft_strcpy : A custom version of _strcpy_ which accepts both the destination and the source strings. The function then copies the source into the destination, only to return the length of the copied characters.

### get_next_line.c functions content :

- get_next_line , ft_gnl1 : the main function of the project.

- ft_fill_s2 : Fills the s2 string with either the string stored by a previous call of GNL, or the read function.

- ft_frees : Frees (if possible) the join structure that allowed the multiples joins.

## 📜 Instructions

To use the function, one must use the "open" function to get the File Descriptor needed by the function. The function can then be called as long as one wants. Once you had fun with it, one needs to close the file with "close".

## 🌐 Resources

The definition of a [static variable](https://en.wikipedia.org/wiki/Static_variable)
Used (with caution) colleagues to undestand the difference between the heap and the stack (or How to prevents lots of leaks).
