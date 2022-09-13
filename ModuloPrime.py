"""
This script recreates the concept of Modulo-Prime upon a 2D Cellular Automaton model (https://en.wikipedia.org/wiki/Cellular_automaton).

The rules of Modulo-Prime, which are primarily defined as a next-state-function to apply to each cell of a 2D grid in each generation to determine its next state,
are simple:
    1. A cell can either be DEAD (black; 0) or ALIVE (pink; 1)
    2. When a cell has an EVEN amount of neighbors that are ALIVE (modulo 2), it will stay or become DEAD
    3. When a cell has an UNEVEN amount of neighbors that are ALIVE (modulo2), it will stay or become ALIVE

Using this simple rule-set, Modulo-Prime is able to duplicate a starting-configuration of cells along the two axis of the grid within a couple of generations, 
subsequentially resulting in the whole grid being filled by duplications of that starting-configuration.
 
A digital heart was chosen as starting-configuration. Love forever, love is freely <3
"""

from CA import CellularAutomaton


# Construct the Cellular-Automaton (CA) model
ca = CellularAutomaton(
        state_colors={0:(0.0,0.0,0.0), 1:(1.0,0.0,0.8)},
        grid_size=(250,250),
        window_size=(750,750)
)


# Supply the grid-init function to the CA to provide a initial configuration of cell-states.
# In this example, A digital heart was chosen as starting-configuration.
@ca.GridInitialize
def init_grid(grid):
    width, height = grid.size
    mid_j, mid_i = int(width/2), int(height/2)
    heart_locs = (  
        (mid_i, mid_j), (mid_i, mid_j-1), (mid_i, mid_j+1),
        (mid_i-1, mid_j), (mid_i-1, mid_j-1), (mid_i+1, mid_j-1),
        (mid_i-1, mid_j+1), (mid_i+1, mid_j+1), (mid_i, mid_j-2),
        (mid_i, mid_j+2), (mid_i-2, mid_j), (mid_i+1, mid_j-2),
        (mid_i+2, mid_j-2), (mid_i+1, mid_j-3), (mid_i+1, mid_j-1),
        (mid_i+1, mid_j+2), (mid_i+2, mid_j+2), (mid_i+1, mid_j+3),
        (mid_i+1, mid_j+1), (mid_i, mid_j-3), (mid_i-1, mid_j-2),
        (mid_i-2, mid_j-1), (mid_i, mid_j+3), (mid_i-1, mid_j+2),
        (mid_i-2, mid_j+1), (mid_i-3, mid_j)
    )
    for loc in heart_locs:
        grid[loc].state = 1

# Supply the next-state-function to the CA, containing the rules by which to update each cell in each frame.
# In this example, the next-state-function follows the rules of Modulo-Prime.
@ca.NextState
def next_state_function(cell):
    nbs = cell.neighbors
    nbs_neuman4 = (int(nb.state) for nb in (nbs[1], nbs[3], nbs[4], nbs[6]))
    return(sum(nbs_neuman4)%2)


# Run the CA model, only when this script is not used as module
if __name__ == '__main__':
    ca.run()