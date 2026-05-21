*This activity has been created as part of the 42 curriculum by maziza.*

---

# Fly-In 🚁

## Description

**Fly-In** is a drone pathfinding simulation built for the 42 curriculum. The goal is to route a fleet of drones through a graph of interconnected hubs — from a designated start hub to an end hub — in as few simulation turns as possible, while respecting per-hub and per-connection capacity constraints.

The project combines graph theory, multi-agent pathfinding, and real-time visual simulation. Maps are described in plain-text configuration files and can range from trivial linear paths to complex topologies with bottlenecks, dead ends, restricted zones, and dozens of concurrent drones.

The simulation runs step by step: at each turn, every drone independently selects the best available next hub based on zone types, link capacities, and the current traffic state. All of this is rendered live in a **Pygame** window where hubs, connections, and animated drones are displayed on screen.

---

## Instructions

### Prerequisites

- Python 3.13+
- A Unix-like system (Linux or macOS) — the Makefile uses `source` and shell chaining

### Installation & Run (recommended)

The Makefile handles virtual environment creation, dependency installation, and execution in one command:

```bash
make
```

This is equivalent to running `make install` followed by `make run`.

### Step-by-step

```bash
# 1. Create the virtual environment and install dependencies
make install

# 2. Run the simulator
make run
```

To run manually without the Makefile:

```bash
python3 -m venv venv_flyin
source venv_flyin/bin/activate
pip install -r requirements.txt
python3 fly_in.py
```

### Linting

```bash
make lint
```

Runs `flake8` (style) and `mypy --strict` (type checking) on all source files.

### Cleanup

```bash
make clean
```

Removes the virtual environment.

### Using the simulator

Once the window opens:

1. **Click a level button** on the main menu to load a map.
2. **Press `SPACE`** to advance one simulation turn — each drone moves to its next chosen hub.
3. **Press `ESC`** to return to the main menu at any time.
4. The turn counter in the top-left updates after each step.
5. The simulation ends automatically when all drones reach the goal hub.

---

## Algorithm Choices & Implementation Strategy

### Graph Pre-processing

Before the simulation starts, the graph is cleaned in two passes (`graph_operations.py`):

1. **Dead-end and unreachable node removal** (`graph_find_useless`): Starting from the start hub, the algorithm expands the reachable set from each neighbour. Any sub-tree that never reaches the goal hub is marked as useless and removed. Nodes tagged `zone=blocked` in the map file are also removed unconditionally.
2. **Stub pruning** (`graph_cleaner`): After the first pass, any node with fewer than two connections (excluding start and goal) is iteratively removed until the graph stabilises. This eliminates orphaned nodes created by previous removals.

This pre-processing ensures the pathfinding algorithm only operates on the reachable, meaningful portion of the graph.

### Path Discovery (`path_finding.py`)

All valid simple paths (no repeated nodes) from start to goal are discovered using a **BFS-style expansion**. Starting from a list containing only the start node, the algorithm appends one new neighbour per iteration, discarding any path that revisits a node, and retains a path as soon as it contains the goal.

The resulting list of paths is sorted by three criteria applied in order (most important last, so the final sort is the tiebreaker):

| Priority | Criterion | Direction | Rationale |
|---|---|---|---|
| 3 (highest) | **Turn cost** (`path_turns`) | Ascending | Minimise total turns; restricted zones cost 2 turns per hop |
| 2 | **Priority zone score** (`path_priorities`) | Descending | Prefer paths passing through priority zones earlier (weighted by position) |
| 1 | **Capacity score** (`path_avg_drone`) | Descending | Prefer paths with higher and more uniform link/hub capacity (mean minus √variance) |

The pre-sorted path list is stored on the `Graph` class and reused by all drones each turn.

### Per-Turn Drone Decision (`drone.py`)

Each drone calls `best_choice()` once per simulation turn. The decision logic proceeds as follows:

1. **Goal check**: if the drone has already reached the goal, it does nothing.
2. **Candidate next hops**: the drone looks at all valid sub-paths reachable from its current position via `better_path()`. For each immediate neighbour not yet visited, it fetches the pre-sorted path continuation from `Graph.get_paths()`.
3. **Congestion filtering**: candidate paths are discarded if the next hub or the connecting link has already reached its capacity limit for this turn (tracked in `Drone.max_paths` and `Drone.max_hubs`).
4. **Path re-ranking**: remaining candidates are re-sorted by the same three criteria used during path discovery, now applied to the remaining sub-path from the drone's current position.
5. **Cost comparison**: the algorithm compares the turn cost of the best alternative against continuing on the current path, factoring in how many other drones are queuing for the same next hop (`get_drone_index`). If the alternative is not actually better, the drone stays on its current path.
6. **Move execution**: the chosen next hub's counters are updated in the shared dictionaries, the drone's position list is extended, and a `D{n}-{hub}` token is added to the turn output string.
7. **Restricted zone handling**: drones entering a restricted zone (`zone=restricted`) have their movement blocked for one additional turn (`self.restricted` flag), simulating the 2-turn cost.

At the end of each turn, `reset_turn_dicts()` resets per-link traffic counters back to zero while preserving the capacity ceilings, ready for the next turn.

### Coordination Model

Drones do not communicate explicitly. Coordination emerges from the shared `max_paths` and `max_hubs` dictionaries, which are updated as each drone makes its decision within a turn. Drones processed earlier in the list have first access to capacity slots; later drones find reduced availability and may select alternative routes. This greedy turn-order mechanism is simple and computationally cheap, though it means the solution quality can depend on drone numbering.

---

## Visual Representation

The visual layer is implemented in `flyin_engine.py` using Pygame's sprite system. All visual elements are `pygame.sprite.Sprite` subclasses grouped in a `pygame.sprite.Group` and drawn each frame.

### Hub Sprites (`GameEngine.GameHub`)

Each hub is rendered as a coloured circle (radius 25 px) with its name displayed below it. The hub's map coordinates are normalised to fit the 1820×880 usable area of the 1920×1080 window, so any graph fills the screen regardless of the coordinate scale used in the map file:

```
screen_x = (coord_x - min_x) × (1820 / (range_x + 1))
screen_y = (coord_y - min_y) × (880  / (range_y + 1))
```

Eighteen named colours are supported; the special `rainbow` colour splits the circle into four quadrants with distinct colours, providing a visually distinctive marker for complex topology hubs.

### Connection Sprites (`GameEngine.GameConnection`)

Each directed edge is drawn as a thick line (10 px) between the centres of its two hub sprites. The line is rendered onto a transparent surface whose bounding box spans the two hubs, then positioned in the scene. Connections are added to the sprite group before hubs so they are drawn beneath them.

### Drone Sprites (`Drone`)

Drones are rendered using `srcs/drone.png` with the drone's number rendered on top of the image. When a drone moves, its pixel position is interpolated over 15 animation frames between the previous and current hub rectangles:

```
pos_x = start_x + (end_x - start_x) × (frame / 15)
pos_y = start_y + (end_y - start_y) × (frame / 15)
```

This smooth animation makes it easy to follow individual drones across the graph.

### Turn Counter (`GameEngine.Turns`)

A persistent overlay in the top-left corner displays the current turn number in white text on a transparent background. It updates every time `SPACE` is pressed.

### Level Select Menu (`GameEngine.MenuScene` / `LevelTitle`)

The main menu renders one clickable button per map file. Buttons are positioned in a fixed grid organised by difficulty column (Easy / Medium / Hard / Challenger / Custom). Hovering a button turns it green; clicking it sets the engine state to `"load"`, which triggers map parsing and scene transition on the next frame.

### Scene Management

Two scene types implement the abstract `GameEngine.Scene` interface: `MenuScene` (main menu) and `LevelScene` (active simulation). The game loop holds a reference to the current scene and calls `update()` + `draw()` each frame, making scene transitions a simple reassignment.

---

## Resources

### Python & Pygame

- [Pygame documentation](https://www.pygame.org/docs/) — official reference for the rendering and event loop.
- [Pydantic v2 documentation](https://docs.pydantic.dev/latest/) — used for hub model validation.
- [Python `functools.partial`](https://docs.python.org/3/library/functools.html#functools.partial) — used for sorting key factories in `path_finding.py`.

### AI Usage

AI assistance (Claude by Anthropic) was used during this project for the following tasks:

- **README generation**: this file was drafted with AI assistance based on a full reading of the source code, map files, and existing documentation.

AI was **not** used for the core algorithm design, the Pygame rendering logic, the map configuration format, or the game loop architecture — those were implemented by the project authors.
