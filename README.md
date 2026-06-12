# Gothic 1 Remake – Lock Pick Solver

A small tool that calculates the shortest sequence of moves to solve
the chest/door lockpicking minigame in **Gothic 1 Remake**.

In this minigame, a chest has several hinges, each with multiple pins.
Moving one hinge can also move other hinges, depending on how they are
mechanically linked. This tool finds the shortest sequence of moves to
get every hinge onto its correct pin without ever hitting a wall
(which would break your lockpick).

## Requirements

- Python 3 (https://python.org – check "Add Python to PATH" during install)
- No additional libraries needed (standard library only)

## Running

```
python lockpick_solver_gui.py
```

or rename the file to `lockpick_solver_gui.pyw` so no console window
opens.

## How to use

1. Set **Hinges** and **Pins per hinge** at the top, then click "Build".
2. In the **Input** section:
   - **Start**: the current pin position of each hinge (1–7)
   - **Goal**: the pin position each hinge needs to reach
   - **Influence Matrix**: for every hinge-to-hinge combination,
     set how moving one hinge affects the other:
     - `+` = moves in the same direction
     - `−` = moves in the opposite direction
     - `0` = no effect
   - Click a cell to cycle through the three states.
3. Click **Calculate solution**.
4. The **Solution** section shows the move sequence, e.g.:
   - `Hinge 3: Pin 4 → Pin 5   H3 – D`
   - `A` = move the hinge left
   - `D` = move the hinge right

Both sections (Input / Solution) can be collapsed and expanded via
their header bar.

## Notes

- A move that would push any hinge past pin 1 or the last pin
  (i.e. hit a wall) is never suggested by the solver.
- The solver always finds the **shortest** solution (breadth-first search).
- If no solution is found, the goal is not reachable from the current
  start position with the given influence matrix.

## Building a standalone .exe (optional)

```
py -m pip install pyinstaller
py -m PyInstaller --onefile --noconsole lockpick_solver_gui.py
```

The finished `.exe` will be located in the `dist/` folder.
