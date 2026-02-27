*This activity has been created as part of 42 curriculum by fvalota, maziza*

# A Maze Ing

    Welcome to the world of maze generation

## Description

In this project we have to generate and solve a maze with a few constraints
We have to read a 'config.txt' file to have the maze info, then display it with some user interaction like regenerating a maze, show/hide a valid shortest path and change the maze colors
We also have to generate an output file with maze representation in hexadecimal, entry and exit coordinates and the shortest path in the form of direction ('N', 'E', 'S', 'W')

## Instructions

To execute the program, simply write:
'''bash
make run
'''
No extra installations needed

You can run a debug mode with:
'''bash
make debug
'''

## Ressources

[Maze Genration Algorithm] (https://en.wikipedia.org/wiki/Maze_generation_algorithm)
[Djikstra Algorithm] (https://www.datacamp.com/fr/tutorial/dijkstra-algorithm-in-python)

## Technical choices

### config.txt

The 'config.txt' file look like this:

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19, 14
OUTPUT_FILE='maze.txt'
PERFECT=False
(SEED='1632490875') (Optional)

'ENTRY' and 'EXIT' must be diffent and in bounds of the maze
If 'PERFECT' is True, the maze should have exactly one path between 'ENTRY' and 'EXIT'
The 'SEED' is optional, a random seed will be generated if none is given

### Maze generation algorithm

Randomized depth-first search:

1. We start with a maze that is full of walls 
2. We create a list of visited cells starting with the bottom-left one of the maze
3. We randomly choose a direction where the next cell is not already visited and we break the wall in this direction
4. We go to the new cell and add it to the visited cells
5. We repeat step 3 and 4 until a cell has no non-visited neighbors or when we reached a certain random (seed) number of steps
6. We bactrack to the previous cells until we find one with unvisited neighbours and back to step 3

We choose this algorithm because of the easy implementation and the 'realistic' way the maze look in the end

## Taks distribution

### fvalota

1. Maze generation algorithm
2. Djikstra algorithm to determine the shortest path from entry to exit
3. Reading the config file
4. Generate the output file
5. Makefile

### maziza

1. Maze generation algorithm
2. Maze display 
3. User interface
4. Main program
5. Many code optimization

## Notes


