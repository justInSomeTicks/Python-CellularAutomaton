"""
This script recreates the turing-complete Game of Life by John Conway (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
by implementing the Game of Life's rules upon a 2D Cellular Automaton model (https://en.wikipedia.org/wiki/Cellular_automaton).

The rules of the Game of Life, which are primarily defined as a next-state-function to apply to each cell of a 2D grid in each generation to determine its next state,
are simple:
    1. A cell can either be DEAD (black; 0) or ALIVE (white; 1)
    2. When a cell is DEAD it will stay DEAD, unless it has exactly three neighbors that are ALIVE (cell is 'born')
    3. When a cell is ALIVE it will become DEAD (under- or overpopulation), unless it has two or three neighbors that are ALIVE (cell is 'sustained')

Using these simple mathematical (but real-life inspired) rules, many diverse patterns can arise due to emergence.
In the end, the patterns that form and the final stable state that arises are purely a result of the initial configuration of the grid.

The Game of Life is a mathematical manifest that displays that complex systems of evolution by means of self-organisation 
can even arise as a result of a very simple set of rules.
"""

from random import choice
from enum import IntEnum

from CA import CellularAutomaton


# Create cell-state variants
class CellState(IntEnum):
    DEAD = 0
    ALIVE = 1


# Create colors corresponding to cell-state variants
COLORS = {
    CellState.DEAD:     (0.0, 0.0, 0.0),
    CellState.ALIVE:    (1.0, 1.0, 1.0)
}


# Construct the Cellular-Automaton (CA) model
ca = CellularAutomaton(
    state_colors = COLORS,
    grid_size = (150, 150),
    window_size = (600, 600)
)


# Supply the grid-init function to the CA to provide a initial configuration of cell-states.
# In this example, the grid will be initialized stochastically DEAD or ALIVE within the middle square of the grid.
@ca.GridInitialize
def grid_init(grid):
    width, height = grid.size
    one_fourth_width, three_fourth_width = (1/4)*width, (3/4)*width
    one_fourth_height, three_fourth_height = (1/4)*height, (3/4)*height 
    for (i,j), cell in grid:
        in_mid_width = one_fourth_width < j <= three_fourth_width
        in_mid_height = one_fourth_height < i <=  three_fourth_height
        cell.state = choice((CellState.DEAD, CellState.ALIVE)) \
            if (in_mid_width and in_mid_height) else CellState.DEAD 

# Supply the next-state-function to the CA, containing the rules by which to update each cell in each frame.
# In this example, the next-state-function follows the rules of John Conway's Game of Life.
@ca.NextState
def next_state_function(cell):
    neighbors_amt = sum(int(nb.state) for nb in cell.neighbors)
    if neighbors_amt == 3 or (neighbors_amt == 2 and cell.state == CellState.ALIVE):
        return CellState.ALIVE
    return CellState.DEAD


# Run the CA model, only when this script is not used as module
if __name__ == '__main__':
    ca.run()