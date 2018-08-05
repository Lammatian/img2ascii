import tkinter as tk

WIDTH = 1000
HEIGHT = 600

MARKER_SMALL = 2
MARKER_MEDIUM = 6
MARKER_BIG = 10

class Paint():
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.last_x = None
        self.last_y = None
        self.is_drawing = False

        self.marker_size = MARKER_MEDIUM

        #self.canvas.bind("<B1-Motion>", self.start_drawing)
        self.canvas.bind("<ButtonPress-1>", self.toggle_draw)
        self.canvas.bind("<ButtonRelease-1>", self.toggle_draw)
        self.canvas.bind("<Motion>", self.draw)
        self.create_toolbar()

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.master, width=WIDTH, height=0.1*HEIGHT, bg="grey")
#        self.small_marker_button = tk.Button(self.toolbar, width=MARKER_SMALL, height=MARKER_SMALL, bg="black")
#        self.small_marker_button.grid(row=0, column=0)
#        self.medium_marker_button = tk.Button(self.toolbar, width=MARKER_SMALL, height=MARKER_SMALL, bg="black")
#        self.medium_marker_button.pack(side=tk.LEFT)
        self.toolbar.pack(side=tk.BOTTOM)

    def toggle_draw(self, event):
        self.is_drawing = not self.is_drawing

    def draw(self, event):
        if self.is_drawing and self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, 
                                    self.last_y, 
                                    event.x, 
                                    event.y, 
                                    width=self.marker_size,
                                    capstyle=tk.ROUND,
                                    smooth=True,
                                    splinesteps=36)

        self.last_x = event.x
        self.last_y = event.y

