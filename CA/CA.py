
from .graphics import pyglet, GraphicsWindow
from .grid import Cell, BoundaryRule, CellularGrid, array


class CellularAutomaton:
    """The cellular-automaton model; prepares and modifies the 2D CellularGrid and its containing Cells
    and displays them to the screen using the GraphicsWindow. In order to run this model, two hooks must
    be defined by the user: one to initialize the grid and one to update a singular cell in each generation 
    using the 'GridInitialize' and 'NextState' descriptors bound to this object.

    state_colors:   dictionary of (int, [float, float, float]) key-value-pairs to denote the state and corresponding RGB color
    grid_size:      size tuple of (width, height)
    window_size:    size tuple of (width, height)
    boundary:       boundary-rule to apply - currently only 'WRAP' is implemented for a transient boundary
    fps_max:        maximal fps to enforce for updating and displaying the model""" 


    def __init__(self, state_colors, grid_size=(200,200), window_size=(600,600), boundary=BoundaryRule.WRAP, fps_max=60):
        """Initialize the 2D Cellular Automaton and its components"""
        # Pyglet applies a color to each vertex; for an uniform color of each cell-square
        # we replicate the RGB value 4 times
        self.state_colors = {state:4*tuple(color) for state, color in state_colors.items()}

        self.window = GraphicsWindow(*window_size, update_hook=self.__update, fps_max=fps_max)
        self.grid = CellularGrid(*grid_size, boundary=boundary)
        self.__hooks = {}
        self.__updatelist = []


    def GridInitialize(self, hook):
        """Set the init-grid hook which is meant to apply a starting configuration of the model.
        The hook will be supplied with one argument: the grid on which to apply the starting config."""
        self.__hooks['init_grid'] = hook

    def NextState(self, hook):
        """Set the next-state-function hook which is meant to calculate the next-state of a singular cell
        and should return this as its output. The hook will be supplied with one argument: the cell of which
        to calculate the next-state."""
        self.__hooks['next_state_function'] = hook



    def run(self):
        """Check the presence of required hooks, prepare the grid, and run the application bound to the window."""
        self.__check_hooks()
        self.__prepare_grid()
        self.window.run()


    def __check_hooks(self):
        """Check for the presence of the required hooks 'init_grid' and 'next_state_function'.""" 
        gridinit_is_set = 'init_grid' in self.__hooks and hasattr(self.__hooks['init_grid'], '__call__') 
        nsf_is_set = 'next_state_function' in self.__hooks and hasattr(self.__hooks['next_state_function'], '__call__')
        if not (gridinit_is_set and nsf_is_set):
            raise Exception("In order to run, the 'init_grid' and 'next_state_function' hooks must be set using the 'GridInitialize' and 'NextState' descriptors bound to this CA-object.")
        
    def __prepare_grid(self):
        """Prepare the grid by calling the user-defined init-grid hook, binding the grid-cells as drawable vertices, and binding the grid-cells together as neighbors."""
        self.__hooks['init_grid'](self.grid)
        self.__bind_grid_vertices()
        self.grid._bind_neighbor_cells()

    def __bind_grid_vertices(self):
        """Bind the grid-cells as drawable vertices to the window by creating an updateable vertex-list for each cell."""
        window_width, window_height = self.window.width, self.window.height
        grid_width, grid_height = self.grid.size
        cell_width, cell_height = window_width/grid_width, window_height/grid_height

        self.__vlists = array([
            array( [None for _ in range(grid_width)] ) \
                for _ in range(grid_height)
        ])

        for state, (i,j), vertices in self.grid._iter_cells_as_vertices(cell_width, cell_height):
            self.__vlists[i][j] = self.window.batch.add_indexed(
                4, pyglet.gl.GL_TRIANGLES, None, [0,1,2,1,2,3],
                ('v2f/static', vertices),
                ('c3f/dynamic', self.state_colors[state])
            )


    def __update(self, dt):
        """Update the state of the model by computating and updating the next-state of each cell using the next-state-function, and modifying the color of the correspondig vertex-list."""
        if self.window.is_paused: 
            return
        nsf = self.__hooks['next_state_function']
        colors = self.state_colors
        updatelist = self.__updatelist
        vlists = self.__vlists
        for (i,j), cell in self.grid:
            state_next = nsf(cell)
            if state_next is not None and state_next != cell.state:
                vlists[i,j].colors = colors[state_next]
                updatelist.append((cell, state_next))
        # Apply the state-changes to the cells after having calculated the next-state of all cells, as means of double-buffering the grid
        while updatelist:
            cell, state_next = updatelist.pop()
            cell.state = state_next


