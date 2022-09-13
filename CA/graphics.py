
import pyglet


class GraphicsWindow(pyglet.window.Window):
    """The GraphicsWindow; encapsulates the pyglet OpenGL Window to be used as updateable screen for the batch-drawing
    of vertices. Includes a fps-display. 
    
    *args:          arguments to be passed to the pyglet Window constructor
    batch:          graphics batch to be used for drawing the vertices
    update_hook:    a predefined function that handles the updating of the vertices to be drawn each frame
    fps_max:        maximal frames-per-second to enforce for updating 
    **kwargs:       keyword-arguments to be passed to the pyglet Window constructor
    """
    
    def __init__(self, *args, batch=pyglet.graphics.Batch(), update_hook=lambda : None, fps_max=60, **kwargs):
        """Initialize the GraphicsWindow and its components."""
        super().__init__(*args, **kwargs)
        self.batch = batch
        self.fps_max = fps_max
        self.fps_display = pyglet.window.FPSDisplay(window=self)
        pyglet.clock.schedule_interval(update_hook, 1.0/fps_max)

        self.is_paused = True

    def on_draw(self):
        """Window-event; update the window by clearing it and drawing the vertices and fps-display."""
        self.clear()
        self.batch.draw()
        if not self.is_paused: self.fps_display.draw()

    def on_mouse_press(self, *_):
        self.is_paused = False if self.is_paused else True

    def run(self):
        """Run the app bound to the window by letting pyglet call the update_hook in intervals of 1/fps_max"""
        pyglet.app.run()
