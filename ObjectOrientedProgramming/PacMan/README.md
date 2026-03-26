*This activity has been created as part of
the 42 curriculum by maziza, fvalota*

# Pacman <img src="/assets/pacman.png" width="20" height="20"> <img src="/assets/pacgum.png" width="20" height="20">  <img src="/assets/pacgum.png" width="20" height="20"> <img src="/assets/pacgum.png" width="20" height="20"> <img src="/assets/eatable.png" width="20" height="20"> 

## Description

This project is part of the 42 projects, and its goals are to teach 2 students to apply all Python notions that have been learned and work together to code from scratch the famous videogame Pacman.

For those who lived in a cave for the last 46 years, Pacman is a videogame about a spherical character ("Pacman") who's main goal is to escape 4 ghosts in a maze while eating little pellets, fruits and sometimes eat the ghosts themselves.

## Instructions

### How to install

To install and play the game, you must follow these steps:

- Download the latest **.zip** release, and extract it

- If you're on Linux, go in the directory, then run the following commands:

```bash
make install
make run
```

This will create a virtual environment, install all needed dependencies for this game to work (`make install`), then run the game with its configuration file (`make run`).

- If you're on Windows, run the following commands:

```powershell
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
python3 main.py config.json
```

## Others

### Configuration

To ensure the maze has base values, we have to give the program a configuration file.\
If the file misses one or more base value, we fill them with default ones.

The config file look like this:  
  
```nano
'highscore_filename': str (default 'highscore.json')  
'side': list[int] (size of the maze: default from 16 to 10 with doubles)  
'dt': list[int] (speed of movement: default 2 and gradually increasing with maze size decreasing)  
'level': int (default 0)  
'lives': int (default 3)  
'points_per_pacgums': int (default 10)  
'points_per_super_pacgums': int (default 50)   
'points_per_ghost': int (default 200)  
'level_max_time': int (default 90)
```

### Highscores

The highscore system is stored in a json file containing a list with a pair [Name, Score]  
We store it this way so every player will have it's own score leaderboard

### Maze Generation

To generate a proper maze for the game to work, we used the mazegenerator attached to the subject by 42. This maze generator takes dimensions (width x height) and a seed to ensure the reproducibility of a maze.

### Implementation

Once the maze is generated, we implemented different things:

- First, we wanted to reproduce the teleportation mechanic that happens in almost every Pacman game, which transport Pacman (and not the ghosts in our version) from left to right and vice versa.

    This implementation gives the player time to breath when the ghosts chase him for a long time without having to eat a SuperPacgum.

- As for the ghosts, we wanted to match a basic behavior found on a wiki (see **Resources**). Here's how:

    - For Blinky <img src="/assets/blinky.png" width="20" height="20"> (the red one), he's an aggressive spirit and always aim at Pacman's position.

    - For Pinky <img src="/assets/pinky.png" width="20" height="20"> (the pink one), she aims (if possible) two tiles in front of Pacman off guard. This aims to put Pacman in a sandwich position between Blinky and Pinky.

    - For Clyde <img src="/assets/clyde.png" width="20" height="20"> (the orange one), he's the odd one out. He's doing the same as Blinky, except that he flees Pacman whenever he's in a 2 tiles radius from him.

    - As for Inky <img src="/assets/inky.png" width="20" height="20"> (the blue one), his original behavior is to copy the vector between Blinky and Pinky's target, and aim at the 180° rotated vector to flank Pacman. Because this aiming pattern was too difficult for us at the moment, we decided to give him a behavior similar to Blinky (might change in the future). 

- As a bonus and immersion choice, we decided to implement sounds from the original game (such as eating the pacgums, the intro, and so on)

- Finally, as expected from the subject, a cheat mode has been added to ease the reviewer's project review. Here are the keys to use it at will:

  <kbd> C </kbd>: Enable Cheat Mode.

  <kbd> L-Ctrl </kbd> + <kbd> C </kbd> : Disable Cheat Mode.

  Once the Cheat Mode is enable, Pacman is intangible (can't die because of the ghosts).\
  Following are the keys you can press to do differents things in Cheat Mode:
  
  - <kbd> M </kbd> key / <kbd> L-Ctrl </kbd> + <kbd> M </kbd> keys: Enable/Disable ghosts movement.
  - <kbd> E </kbd> key: Enable the ghosts "Flee" state.
  - <kbd> G </kbd> key: Automatically win the game. 
  - <kbd> - </kbd> keypad key: Automatically lose the game. 
  - <kbd> 0 - 9 </kbd> keypad keys / <kbd> 1 - 0 </kbd> keys : switch to the desired level (0 being the first and 9 the last. 

### Architecture

The game architecture was rethought many time through development, but here is the main one:

The game loop runs in a while loop, checking for events, like 'Pause', 'Game Over' or 'Next Level'.

Once the maze is generated (as a matrix), a Wall class handle displaying them on the screen, based on their coordinate.

Following this, a Pacgum Class handle placing the Pacgums and SuperPacgums in the maze, while not placing them where Pacman, the ghosts or the 42 walls are.

Then, a Pacman Class, a Ghost class and its children (Blinky, Pinky and Clyde), all inheriting from a pygame Sprite class, handle the game objects, where they spawn, and how the behave in the maze. For instance, They all store their maze coordinates (in a tuple form (x, y) where the maximum x and y are the size of the maze, and their screen coordinates (in pixels).\
- Their maze coordinates allow to handle the 'walls collisions', which are checked by comparing a maze cell and the object coordinate.\
- Their pixel coordinate allow to handle their movement throughout the game.

Finally, all the display part is handled with various functions that create pygame Surfaces ready to be applied to the screen whenever their turn comes.

### Project Management

Here is the Project organization and how tasks were dealed.

<img src="/assets/diagram.png" width="618" height="815">

and a small evolution timelapse

<img src="/assets/evolution.gif" width="618" height="480">

## Ressources

[Original game](https://freepacman.org/)

[Pygame doc](https://www.pygame.org/docs/)

[Ghost behavior inspiration](https://pacman.fandom.com/wiki/Maze_Ghost_AI_Behaviors)

[Graph maker](https://online.visual-paradigm.com/)

[Advanced ghost behavior video](https://www.youtube.com/watch?v=ataGotQ7ir8&list=WL&index=6) (future goal of development)
