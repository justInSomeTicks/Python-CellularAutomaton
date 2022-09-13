# PY_2DCellularAutomaton
This project aimed to create a minimal framework for making 2-dimensional Cellular Automata in python (https://en.m.wikipedia.org/wiki/Cellular_automaton). The Cellular Automaton model is implemented as a grid of square cells, each of which hold a certain state at a certain generation. The state-changes are determined by the next-state function applied to each cell, which defaultly takes into consideration the states of the local 'neighbors'. Using specialized next-state functions, one is able to generate global emergent patterns from simple mathematical rules.

## Installation
The only dependency of this project is pyglet, a python wrapper for OpenGL, which you can install it through `pip install pyglet`. See the following page for more info: https://pyglet.readthedocs.io/en/latest/programming_guide/installation.html.

## Content and demonstration
This project contains the following toplevel units:
- `CA` [folder]: contains the Cellular-Automaton module and back-end, and exports the available classes, of which most importantly the 'CellularAutomaton' class functioning as the main interface of the model.


- `GameOfLife.py` [script]: demonstrates the implementation of the Cellular-Automaton by emulating John Conway's 'Game of Life' (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

![](https://github.com/justinsomechars/Python-CellularAutomaton/blob/main/GameOfLife_demo.gif)

*GIF demonstration of GameOfLife.py*


- `ModuloPrime.py` [script]: demonstrates the implementation of the Cellular-Automaton by another mathematical rule-set, that replicates an initial configuration along both axis indefinitely.

![](https://github.com/justinsomechars/Python-CellularAutomaton/blob/main/ModuloPrime_demo.gif)

*GIF demonstration of ModuloPrime.py*

## Usage
As seen from the `GameOfLife.py` and `ModuloPrime.py` demonstrations, the general routine of using the Cellular-Automaton module goes as follows:
- import the `CellularAutomaton` class from the `CA` module
- define a dictionary with (state, float_rgb_color) key-value-pairs, to be used to define the cells
- construct the `CellularAutomaton` object, passing along the state-colors dictionary and other optional arguments
- bind a init-grid function to the `CellularAutomaton` object through the descriptor `@ca_object.GridInitialize` accepting the grid (indexable) as single argument.
- bind a next-state function to the `CellularAutomaton` object through the descriptor `@ca_object.NextState` accepting the cell to determine the next state of as a single argument. Neighbors of this cell are accessible through the `cell.neighbors` attribute, and the next-state function should return the next-state of the cell, instead of modifying it itself (due to required double buffering of the cell states, which happens in the back-end).
- run the model through `ca_object.run()`!

## Notes 
- This repository was created for resume/portfolio purposes.
- this module was not optimized for efficiency (yet?), and shows a simple, minimalistic implementation of a Cellular-Automaton model.
- it was pursued to have the source code of the module acceptably documented (comments/docstrings), but might not follow the full set of PEP8 guidelines.
