import tkinter as tk
import random
from tkinter import messagebox

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.is_obstacle = False

    def __repr__(self):
        return f"({self.x}, {self.y})"

class AStar:
    def __init__(self, start, end, grid):
        self.start = start
        self.end = end
        self.grid = grid
        self.open_list = []
        self.closed_list = []

    def get_distance(self, node_a, node_b):
        return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

    def get_neighbors(self, node):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = node.x + i
                y = node.y + j
                if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]):
                    continue
                if self.grid[x][y].is_obstacle:
                    continue
                neighbors.append(self.grid[x][y])
        return neighbors

    def get_path(self):
        node = self.end
        path = []
        while node is not None:
            path.append(node)
            node = node.parent
        return path[::-1]

    def run(self):
        self.open_list.append(self.start)
        while self.open_list:
            current_node = min(self.open_list, key=lambda x: x.f)
            self.open_list.remove(current_node)
            self.closed_list.append(current_node)
            if current_node == self.end:
                return self.get_path()
            for neighbor in self.get_neighbors(current_node):
                if neighbor in self.closed_list:
                    continue
                new_g = current_node.g + self.get_distance(current_node, neighbor)
                if neighbor not in self.open_list:
                    self.open_list.append(neighbor)
                elif new_g >= neighbor.g:
                    continue
                neighbor.parent = current_node
                neighbor.g = new_g
                neighbor.h = self.get_distance(neighbor, self.end)
                neighbor.f = neighbor.g + neighbor.h
        return None

class Grid:
    def __init__(self, rows, cols, obstacles):
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles
        self.grid = [[Node(i, j) for j in range(cols)] for i in range(rows)]
        self.start = self.grid[0][0]
        self.end = self.grid[8][0]
        self.set_obstacles()
# fixer les obstacles 
    def set_obstacles(self):
        for i in range(self.obstacles):
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            self.grid[x][y].is_obstacle = True

class Application:
   
    def __init__(self, start_coords, end_coords):
        self.window = tk.Tk()
        self.grid = Grid(10, 10, 20)
        self.grid.start = self.grid.grid[start_coords[0]][start_coords[1]]
        self.grid.end = self.grid.grid[end_coords[0]][end_coords[1]]
        self.canvas = tk.Canvas(self.window, width=500, height=500)
        self.draw_grid()
        self.path = []

        # Ajout de deux Entry widgets pour les coordonnées de départ et d'arrivée
        self.start_entry = tk.Entry(self.window)
        self.start_entry.insert(tk.END, f"{start_coords[0]}, {start_coords[1]}")
        self.start_entry.pack()
        self.end_entry = tk.Entry(self.window)
        self.end_entry.insert(tk.END, f"{end_coords[0]}, {end_coords[1]}")
        self.end_entry.pack()

        # Bouton pour lancer la recherche de chemin avec les coordonnées entrées par l'utilisateur
        self.button = tk.Button(self.window, text="Trouver le chemin", command=self.on_button_click)
        self.button.pack()

    def on_button_click(self):
        start_coords = [int(coord) for coord in self.start_entry.get().split(",")]
        end_coords = [int(coord) for coord in self.end_entry.get().split(",")]
        self.grid.start = self.grid.grid[start_coords[0]][start_coords[1]]
        self.grid.end = self.grid.grid[end_coords[0]][end_coords[1]]
        self.draw_grid()
        self.run()

    
    def draw_grid(self):
        cell_width = 50
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                x1 = j * cell_width
                y1 = i * cell_width
                x2 = x1 + cell_width
                y2 = y1 + cell_width
                if self.grid.grid[i][j].is_obstacle:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                elif self.grid.grid[i][j] == self.grid.start:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                elif self.grid.grid[i][j] == self.grid.end:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-2>", self.on_clear)

    def on_click(self, event):
        x = event.x // 50
        y = event.y // 50
        self.grid.grid[y][x].is_obstacle = not self.grid.grid[y][x].is_obstacle
        self.draw_grid()

    def on_clear(self, events):
        self.grid = Grid(10, 10, 15)
        self.draw_grid()

    def run(self):
        astar = AStar(self.grid.start, self.grid.end, self.grid.grid)
        self.path = astar.run()
        if self.path:
            for node in self.path:
                x1 = node.y * 50
                y1 = node.x * 50
                x2 = x1 + 50
                y2 = y1 + 50
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
        else:
            messagebox.showinfo("No path found.")
        self.canvas.mainloop()

start_coords = (0, 0)
end_coords = (7, 6)

app = Application(start_coords, end_coords)
app.run()

