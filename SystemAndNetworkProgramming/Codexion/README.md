*This activity has been created as part of
the 42 curriculum by maziza*

# Codexion

## Description

This project is part of the 42 projects, and its goal is to teach how to handle **threads**, **mutexes** and **shared resources** in C, without ever falling into a deadlock, a starvation or a data race.

For those who never heard of the Dining Philosophers: Codexion is the same idea, with a developer twist. A group of coders sits around a table, with one USB dongle between each pair of neighbours. To work, a coder needs **both** dongles next to him. Every coder repeats the same cycle:

**compile** (needs 2 dongles) → **debug** → **refactor** → back to compile

But there is a catch: a coder who stays too long without compiling **burns out**, and the simulation stops right away. Also, once a dongle has been used, it needs a **cooldown** before anybody can use it again.

The simulation ends in one of two ways:

- Every coder compiled at least `number_of_compiles_required` times (success).
- One coder burnt out (failure).

To make it harder, dongles are not given at random: a **scheduler** (`fifo` or `edf`) decides which coder gets the dongle next.

Here's the overview of how it works:

- One thread per coder, one dongle per coder (`N` coders, `N` dongles).
- One extra **supervisor thread** (the monitor), which is the only one allowed to print.
- Each dongle has its own mutex and its own 2-slot waiting queue.
- Time is measured in milliseconds since the start of the simulation.

## Instructions

### Requirements

- A Linux machine (the code includes `bits/` headers)
- `cc` (gcc or clang) and `make`
- `valgrind` (optional, only for `make val`)

### How to compile

```bash
make codexion
```

This builds the `codexion` executable (flags: `-Wall -Wextra -Werror -pthread -g`).

Other rules:

- `make` : builds the program **and** runs a demo (`./codexion 4 100 5 3 2 2 5 fifo`). Be careful, it also clears your terminal.
- `make clean` : removes the object files (`prefiles/`).
- `make fclean` : removes the objects and the executable.
- `make re` : `fclean` then `all`.
- `make val` : runs the demo under `valgrind --leak-check=full`.

### How to run

```bash
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

| Argument | Type | Meaning |
|---|---|---|
| `number_of_coders` | int | Number of coders (and of dongles). Can't be 0. |
| `time_to_burnout` | int (ms) | Max time between the start of two compiles (or the start of the simulation and the first one). |
| `time_to_compile` | int (ms) | Time a coder spends compiling, holding both dongles. |
| `time_to_debug` | int (ms) | Time a coder spends debugging. |
| `time_to_refactor` | int (ms) | Time a coder spends refactoring. |
| `number_of_compiles_required` | int | Number of compiles every coder must do for the simulation to succeed. |
| `dongle_cooldown` | int (ms) | Time a dongle stays unavailable after being released. |
| `scheduler` | `fifo` or `edf` | Policy used to choose who gets a dongle next. |

The program refuses to start if:

- The number of arguments isn't exactly 8.
- One of the 7 first arguments isn't a positive integer.
- The scheduler isn't `fifo` or `edf`.
- The number of coders is 0.
- `time_to_burnout < time_to_compile + time_to_debug + time_to_refactor + dongle_cooldown` (a coder could burn out even when nothing goes wrong).

### Examples

```bash
./codexion 4 100 5 3 2 2 5 fifo     # 4 coders, FIFO scheduler
./codexion 5 200 10 5 5 3 5 edf     # 5 coders, EDF scheduler
./codexion 1 100 5 3 2 2 5 fifo     # a lonely coder (he will burn out)
```

### Output

Every line follows the format `timestamp_in_ms coder_id message`, with a different color for each state:

```
13 4 got dongles
13 4 got dongles
13 4 is compiling
18 4 is debugging
18 2 got dongles
18 2 got dongles
18 2 is compiling
21 4 is refactoring
```

Notes:

- `got dongles` is printed twice, once for each dongle taken.
- Coder ids start at 1.
- A burnout is printed as `timestamp id burnt out !` and ends the simulation.
- If everyone is done, the program ends with `Success: All threads compiled`.
- There's a 1 second warm-up before the simulation starts, so every thread is created before the clock starts (the timestamps start at 0 after it).

### Project files

| File | Role |
|---|---|
| `main.c` | Arguments check, threads creation / join, log buffer initialization |
| `parser.c` | Arguments parsing, allocation of coders and dongles |
| `thread.c` | Coder routine (compile → debug → refactor) |
| `compile.c` | Waiting for the dongles, compile step, dongle release, burnout detection |
| `debug.c` / `refactor.c` | The two remaining steps of the cycle |
| `queue.c` | Dongle waiting queue, `fifo` and `edf` schedulers |
| `supervisor.c` | Log buffer (`change_status`) and monitor thread (`supervise`) |
| `time_management.c` | Timestamps and time arithmetic |
| `utils.c` | `custom_timedwait`, helper functions |
| `free_mallocs.c` | Memory cleaning |
| `structs.h` / `header.h` / `colors.h` | Structures, prototypes, colors |

## Blocking cases handled

### Deadlock prevention (Coffman's conditions)

A deadlock needs 4 conditions at the same time (Coffman, 1971). Here's how each of them is handled:

- **Mutual exclusion**: kept on purpose, because a dongle can't be shared. A dongle has only one owner at a time (`to_who`).
- **Hold and wait**: limited. A coder never works with a single dongle. He only logs `got dongles` and starts compiling when **both** dongles are assigned to him (the `wait()` loop in `compile.c`).
- **No preemption**: kept. A dongle changes owner only when its current owner releases it, never before.
- **Circular wait**: broken. Each coder sorts his two dongles by index (`swap` in `thread_function`) and always asks for the lowest one first. The last coder, who sits between dongle `N-1` and dongle `0`, asks for dongle `0` first, which opens the circle. This is the classic *resource ordering* solution to the Dining Philosophers.

And as a safety net: nobody can wait forever. If something goes wrong and a coder waits too long, he **burns out**, which is detected, printed, and ends the simulation instead of freezing it.

### Starvation prevention

- Each dongle is only shared by **two** coders, so its waiting queue has only **2 slots**.
- The owner of a dongle chooses the next one when he releases it (**hand-off**), so nobody can sneak in and steal a dongle. A coder who just released a dongle goes **behind** his neighbour in the queue, which prevents him from taking it again immediately.
- The choice of the next owner depends on the scheduler:
  - `fifo`: first to arrive in the queue is the first served.
  - `edf` (Earliest Deadline First): the coder whose burnout deadline (`last compile start + time_to_burnout`) is the closest is served first. The more a coder waits, the more urgent he becomes.

### Cooldown handling

When a coder releases a dongle, the dongle stores the timestamp `now + dongle_cooldown`. A coder who wants it has to wait until this timestamp is passed:

- The waiting is done by `custom_timedwait`, which sleeps until an **absolute** time (and returns immediately if it's already passed).
- Once both cooldowns are over, the coder checks that the timestamps of both dongles **didn't change** while he was sleeping (`is_ts_same`). If one did, he waits again. This way, he never starts compiling with a dongle that was released again in the meantime.
- The burnout is checked in each turn of this loop, so the cooldown never makes a coder miss his deadline silently.

### Precise burnout detection

- Each coder keeps his own **absolute deadline** (`spec`), computed with `clock_gettime` (nanosecond resolution): the start of his last compile + `time_to_burnout`.
- While a coder is waiting for his dongles, he doesn't sleep blindly. He checks his deadline in a tight loop (`has_burnt_out`), so the burnout is detected as soon as it happens, not at the next wake-up.
- The coder who burns out sends a `FAILURE` message to the supervisor, which prints it and raises the `failure` flag. All the other coders see this flag after each of their steps and stop.
- The sanity check at launch (`time_to_burnout >= compile + debug + refactor + cooldown`) makes sure a coder can't burn out while he's actually working.

### Log serialization

- **Coders never print.** They write a `t_log` (timestamp, id, state) in a shared array, and only the supervisor reads it and prints it.
- The timestamp is taken **inside** the critical section, right when the message is stored. So the order of the messages in the array is the real chronological order, and the output can't be mixed up or interleaved (no line cut in the middle by another thread).
- The array is sized in advance: `(4 × number_of_compiles_required + 1) × number_of_coders` messages (4 states per compile, plus one final `SUCCESS` / `FAILURE` per coder), so it never needs to grow while threads are using it.

### Edge cases

- **Only 1 coder**: there's only one dongle, so he can never get two of them. He waits until his burnout and is declared burnt out at `time_to_burnout` (no freeze, no crash).
- **Invalid parameters**: refused before any thread is created (see *Instructions*).
- **Clean exit**: the main thread waits for the supervisor, then joins every coder, destroys the dongle mutexes and frees all the memory (checked with `valgrind`).

## Thread synchronization mechanisms

### Primitives used

| Primitive | Where | Role |
|---|---|---|
| `pthread_mutex_t mutex_dongle` | One per dongle (`t_dongle`) | Protects the dongle owner (`to_who`), its waiting queue and its cooldown timestamp. |
| `pthread_mutex_t mutex_status` | One, shared (`t_status`) | Protects the log array and its write index. |
| `pthread_cond_t cond_status` | One, shared (`t_status`) | Wakes up the supervisor each time a coder posts a new message. |
| `custom_timedwait` | `utils.c` | Home-made timed event: sleeps until an absolute timestamp (cooldown end). |
| `start` / `failure` flags | `t_data` | Start signal for all the coders, and stop signal for the whole simulation. |
| `pthread_create` / `pthread_join` | `main.c` | Life cycle of the N coder threads and the supervisor thread. |

### How the shared resources are protected

**Dongles.** The queue, the owner (`to_who`) and the timestamp of a dongle are only modified inside a `mutex_dongle` critical section (`update_queue_infos` + `next_coder`). Since only two coders can touch a given dongle, a lock is only ever contested by two threads. Each coder locks one dongle at a time and never holds two mutexes at once, so the mutexes can't deadlock between each other.

**Logging.** All messages go through `change_status`, which locks `mutex_status`, stamps the time, stores the message, increments the index, **broadcasts** `cond_status` and unlocks.

**Monitor state.** The `failure` flag is only raised by the supervisor, once it has seen (and printed) a `FAILURE` message. Coders only read it, after each step, and stop when it's set. Each coder also owns his private data (his deadline, his compile counter, his copy of the parameters), so there's nothing to share there.

### Coders ↔ Monitor communication

```
  coder 1 ──┐                                    ┌── prints in order
  coder 2 ──┼─► change_status() ─► log array ─►  │   supervise()
  coder N ──┘   lock mutex_status                │   cond_wait(cond_status)
                write message                    └── sets data->failure on FAILURE
                cond_broadcast
                unlock
```

It's a classic **producer / consumer**: coders produce messages, the supervisor consumes them.

- The supervisor holds `mutex_status` and sleeps in `pthread_cond_wait` while the next slot of the array is still `INIT` (empty). The wait is inside a `while`, so a spurious wake-up can't make it read an empty slot.
- Coders wake it up with `pthread_cond_broadcast` after each message.
- When a `FAILURE` message is read, the supervisor sets `failure` and stops, then the coders notice it and leave their loops.

### Examples of race conditions prevented

1. **Two coders release the same dongle at the same time.** Both want to put themselves in the dongle queue and change `to_who`. Without a lock, one update could erase the other and the dongle would be given to the wrong coder (or to nobody). With `mutex_dongle`, the updates happen one after the other, and the queue always stays coherent.
2. **Two coders print at the same time.** Without serialization, `printf` calls could be mixed, or timestamps could be out of order (a thread stamped at 52 but printed after another stamped at 53). Here the stamp and the storing are one atomic step under `mutex_status`, and a single thread prints.
3. **A coder starts before the others exist.** The coders wait for the `start` flag, which the main thread only sets once all of them are created. They all begin at the same moment, with the same clock reference.
4. **Compiling with a dongle that was reassigned.** The timestamp check (`is_ts_same`) detects that a dongle changed hands during the cooldown wait, and sends the coder back to waiting.
5. **Working while the simulation is already over.** After each step (compile, debug, refactor), the coder checks `failure` and leaves immediately if someone burnt out.

## Resources

### Documentation and references

- [POSIX Threads Programming (LLNL tutorial)](https://hpc-tutorials.llnl.gov/posix/)
- [Operating Systems: Three Easy Pieces, Concurrency chapters (OSTEP)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- `man pthread_create`, `man pthread_mutex_lock`, `man pthread_cond_wait`, `man clock_gettime`, `man usleep`
- E. G. Coffman, M. J. Elphick, A. Shoshani, *System Deadlocks*, ACM Computing Surveys, 1971 (the four conditions)
- E. W. Dijkstra, *Hierarchical ordering of sequential processes* (EWD310), 1971 (Dining Philosophers and resource ordering)
- C. L. Liu, J. W. Layland, *Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment*, 1973 (Earliest Deadline First)
- [Valgrind manual (memcheck and helgrind)](https://valgrind.org/docs/manual/manual.html)

### How AI was used

- **README**: this file was written with the help of an AI assistant (Claude), from the source code of the project and from my previous README, to copy its structure and writing style. I checked its content against the code and ran the program on several scenarios (normal run, `fifo` / `edf`, single coder, bad arguments, burnout).
- **[TO COMPLETE]** Describe here, honestly, which other tasks (if any) used AI, and for which parts of the project (for example: understanding a concept, finding a bug, reviewing the code, writing tests). If AI wasn't used for the code, say it.
