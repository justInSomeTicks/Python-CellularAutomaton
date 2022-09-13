
from enum import IntEnum
from numpy import array

class Cell:
    """The atomic component of the CellularGrid, and thereby the Cellular Automaton model.
    Implemented as slotted object to reduce memory requirements, thereby optimize for the creation
    of a lot of Cells. The slots include the Cell's state and the Cell's neighbors.
    
    The Cell is initialized without arguments, and takes on the state of the default_state class attribute.
    The neighbors slot is initially empty, but is filled by the CellularGrid to functionally bind Cells together."""
    
    __slots__ = ('state', 'neighbors')
    default_state = 0

    def __init__(self):
        """Initialize the Cell by setting the state to default."""
        self.state = self.__class__.default_state


#TODO: implement other boundary-rules
class BoundaryRule(IntEnum):
    """The rules of the boundary to enforce upon the CellularGrid. Currently only WRAP is implemented."""
    WRAP = 0    # Creates an infinite grid by binding the left side with the right side, top with bottom, and both vice versa



class CellularGrid:
    """The CellularGrid; contains the Cells of the model on a 2D grid and enforces boundary-rules
    when binding Cells together as neighbors. Implements convenient iteration of the grid's cells and
    their locations through __iter__ and single cell indexing by __getitem__.

    width:      width of the grid
    height:     height of the grid
    boundary:   boundary-rule to enforce"""

    def __init__(self, width, height, boundary=BoundaryRule.WRAP):
        """Initialize the CellularGrid with certain size (widht, height) and boundary-rule."""
        self.boundary = boundary
        self.size = (width, height)
        self.cells = array([ 
            array( [Cell() for _ in range(width)] ) \
                for _ in range(height) 
        ])

    def __iter__(self):
        """Iterate through the grid's Cells and their locations."""
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                yield (i,j), cell

    def __getitem__(self, loc):
        """Get the cell at a specific i,j location through indexing."""
        return self.cells[loc]


    
    def __get_neighbors(self, i, j):
        """Get the neighbors of a specific cell, given the set boundary-rule.
        Currently only the Moore neighborhood is implemented."""
        if self.boundary == BoundaryRule.WRAP:
            next_j = j+1 if j != self.size[0]-1 else 0 # conjoin right- with left-side
            next_i = i+1 if i != self.size[1]-1 else 0 # conjoin bottom with top
            return (
                self.cells[i-1][j-1], self.cells[i-1][j], self.cells[i-1][next_j],
                self.cells[i][j-1], self.cells[i][next_j],
                self.cells[next_i][j-1], self.cells[next_i][j], self.cells[next_i][next_j]
            )
        else:
            #TODO: implement other boundary-rules
            raise NotImplementedError(f'No implementation for boundary rule {self.boundary}')


    def _bind_neighbor_cells(self):
        """Bind each cell together with its neighbors. 
        Currently only the Moore neighborhood is implemented."""
        for (i,j), cell in self:
            cell.neighbors = self.__get_neighbors(i,j)

    def _iter_cells_as_vertices(self, cell_width, cell_height):
        """Iterate through all the cells and yield the (state, location, vertex_positions)."""
        for (i,j), cell in self:
            yield ( 
                cell.state,
                (i,j), 
                (
                    j*cell_width, i*cell_height,
                    j*cell_width, (i+1)*cell_height,
                    (j+1)*cell_width, i*cell_height,
                    (j+1)*cell_width, (i+1)*cell_height,
                )
            )



