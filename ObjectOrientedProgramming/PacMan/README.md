*This activity has been created as part of
the 42 curriculum by maziza, fvalota*

# Pacman

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
