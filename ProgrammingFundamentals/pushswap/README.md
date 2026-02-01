_This project has been created as part of the 42 curriculum by jenicola, maziza_

# 📚 Project : Push-Swap

## 🔍 Description

The Push-Swap project is a 42 project aiming to teach algorithmic complexity. It introduces complexity notation (big O) and general concepts of optimization.

Given two stacks, one containing unsorted random numbers, one empty, the Push-Swap algorithm must sort the first stack using as little operations as possible, the latter being:

- **push** : sending the top number of one stack to the other.
- **swap** : swaps the two top elemments of a stack between them.
- **rotate** : send the top element of a stack to the bottom, simulating a stack rotation.
- **reverse rotate** : brings the bottom element of a stack to the top, simulating a stack rotation.

To determine which sorting algorithm Push-Swap uses, we calculate the stack disorder, which represents how out of order each element is in the list ; this expression is a percentage which we can use in order to define whether we should use **low**, **medium** or **high** complexity algorithms.

As a general rule, more _efficient_ algorithms tend to pay a **_bigger price upfront_**, making it so simple algorithms tend to behave better in low complexity situations, medium-complexity algorithms in medium-level complexity, and so on.

We use three main algorithms in this implementation of push_swap : **Minmax** for O(n²), a **Bucket** sort for O(n√n), and a **Radix** sort over indexes for an O(nlog(n)) complexity.

## 📁 Content

### ft_strings.h | ft_memory.h

Utility files for memory, text and input treatments.

### pushswap.h

Uses utilities to transform the text input to the program into a properly formed stack.

### ft_stack.h

Includes all of the logic around linked list representing the stacks, with associated functions (creating, adding, removing, stack operations, etc).

### ft_algorithms.h

All used algorithms to sort the stack

### ft_printf.h

Custom [printf project](https://github.com/MatanAziza/Printf) (also part of 42 Common Core)

### ft_output.h

All outputs and its optimization.

### ft_bench.h

When used as a flag during the program execution, create a benchmark that contains all sort of stats.

### ft_errors.h

Treats all kinds of errors that one can encounter during the program execution.

## 📜 Instructions

To use this library, one must execute the `make` command, followed by the following flags to compile the latter :

`make all` : Compile all the **.c** files into their corresponding **.o** files, which are then compiled into a **push_swap** program.

`make clean` : Deletes the `build` folder, which contains all the **.o** files.

`make fclean` : Execute the `make clean` process, and deletes the **push_swap** program as well.

`make re` : Execute the `make fclean` process, followed by the `make all` one.

## 🌐 Resources

[Big O explanation](https://en.wikipedia.org/wiki/Big_O_notation)

[Radix Sort Explanation](https://en.wikipedia.org/wiki/Radix_sort)

[Bucket Sort Explanation](https://en.wikipedia.org/wiki/Bucket_sort)

[Different types of sorting](https://youtu.be/GMV7ycKZ-mM?si=0nzpKa6O_cON8CzA)

![](https://hypixel.net/attachments/1694979/)
