import tkinter as tk
import random
from tkinter import messagebox
from tkinter import Tk, simpledialog

class Node:
    def __init__(self, x, y):
        self.x = x              # coordonnée x du noeud
        self.y = y              # coordonnée y du noeud
        self.parent = None      # noeud parent dans le chemin trouvé
        self.g = 0              # coût depuis le noeud de départ pour arriver à ce noeud
        self.h = 0              # estimation du coût pour aller du noeud courant au noeud d'arrivée
        self.f = 0              # coût total : g + h
        self.is_obstacle = False   # indicateur pour savoir si le noeud est un obstacle

    def __repr__(self):
        return f"({self.x}, {self.y})"

class AStar:
    def __init__(self, start, end, grid):
        self.start = start          # noeud de départ
        self.end = end              # noeud d'arrivée
        self.grid = grid            # grille de noeuds
        self.open_list = []         # liste des noeuds à explorer
        self.closed_list = []       # liste des noeuds explorés

    def get_distance(self, node_a, node_b):
        return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)   # distance de Manhattan

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
            current_node = min(self.open_list, key=lambda x: x.f)   # sélectionne le noeud ayant le coût total f le plus faible
            self.open_list.remove(current_node)
            self.closed_list.append(current_node)
            if current_node == self.end:        # si le noeud courant est le noeud d'arrivée, on a trouvé un chemin
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
        """
        Initialise une grille de noeuds de taille rows * cols.
        Chaque noeud est un objet de la classe Node.
        obstacles est le nombre de cases qui seront marquées comme obstacles.
        """
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles
        
        # Crée la grille de noeuds
        self.grid = [[Node(i, j) for j in range(cols)] for i in range(rows)]
        
        # Initialise le noeud de départ et le noeud de fin à None
        self.start = None
        self.end = None
        
        # Place les obstacles aléatoirement sur la grille
        self.set_obstacles()

    def set_obstacles(self):
        
        #Place les obstacles aléatoirement sur la grille.
        
        for i in range(self.obstacles):
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            self.grid[x][y].is_obstacle = True
    
    def set_start(self, x, y):
        
        #Définit le noeud de départ.
        
        self.start = self.grid[x][y]

    def set_end(self, x, y):
        
        #Définit le noeud de fin.
        
        self.end = self.grid[x][y]



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # Demander à l'utilisateur de saisir la taille de la grille (entre 5 et 20)
        size = simpledialog.askinteger("Taille de la grille", "Entrez la taille de la grille (entre 5 et 20)", minvalue=5, maxvalue=20)
        
        # Créer la grille avec la taille saisie et un nombre d'obstacles proportionnel à la taille (10% de la surface totale)
        
        obstacles = int(size * size * 0.1) # calculer le nombre d'obstacles
        
        # Créer la grille avec la taille et le nombre d'obstacles définis
        
        self.grid = Grid(size, size, obstacles)

        # Adapter la taille du canvas en fonction de la taille de la grille
        
        self.canvas = tk.Canvas(self.master, width=size * 25, height=size * 25)
        self.canvas.pack()
        self.button = tk.Button(self.master, text="Find path", command=self.find_path)
        self.button.pack()
        self.draw_grid()
        self.start = None
        self.end = None
        self.path = None
        self.canvas.bind("<Button-1>", self.select_node)
        self.canvas.bind("<Button-3>", self.add_obstacle)

    def add_obstacle(self, event):
        i = event.x // 25
        j = event.y // 25
        node = self.grid.grid[i][j]
        node.is_obstacle = True
        x1 = i * 25
        y1 = j * 25
        x2 = x1 + 25
        y2 = y1 + 25
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")


    def draw_grid(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                node = self.grid.grid[i][j]
                x1 = node.x * 25
                y1 = node.y * 25
                x2 = x1 + 25
                y2 = y1 + 25
                if node.is_obstacle:
                    color = "black"
                else:
                    color = "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    
    def select_node(self, event):
        i = event.x // 25
        j = event.y // 25
        node = self.grid.grid[i][j]
        color = "white" # Valeur par défaut pour color
        if not node.is_obstacle:
            if self.path is not None: # effacer le chemin précédent
                for node in self.path:
                    i = node.x
                    j = node.y
                    x1 = i * 25
                    y1 = j * 25
                    x2 = x1 + 25
                    y2 = y1 + 25
                    if node != self.start: # ne pas effacer le point de départ
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                self.path = None # réinitialiser le chemin

            if self.start == node: # le nœud cliqué est le point de départ
                color = "green"
            elif self.end == node: # le nœud cliqué est le point d'arrivée
                self.end = None # réinitialiser le point d'arrivée
                color = "white"
            elif self.start is None: 
                self.start = node
                color = "green"
            elif self.end is None: # le nœud cliqué devient le point d'arrivée
                self.end = node
                color = "red"
            else: # le nœud cliqué ne peut pas être sélectionné
                return

            x1 = i * 25
            y1 = j * 25
            x2 = x1 + 25
            y2 = y1 + 25
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    def find_path(self):
        if self.start is not None and self.end is not None:
            astar = AStar(self.start, self.end, self.grid.grid)
            new_path = astar.run()
            if new_path is not None:
                if self.path is not None: # effacer le chemin précédent
                    for node in self.path:
                        i = node.x
                        j = node.y
                        x1 = i * 25
                        y1 = j * 25
                        x2 = x1 + 25
                        y2 = y1 + 25
                        if node != self.start and node != self.end: # ne pas effacer les points de départ et d'arrivée
                            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                self.path = new_path # mettre à jour le chemin
                for node in self.path:
                    i = node.x
                    j = node.y
                    x1 = i * 25
                    y1 = j * 25
                    x2 = x1 + 25
                    y2 = y1 + 25
                    if node != self.start and node != self.end: # ne pas colorier les points de départ et d'arrivée
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
            else:
                messagebox.showerror("Erreur", "Aucun chemin trouvé !")

    def run(self):
        self.master.mainloop()

# Création de l'instance de la classe Tk
root = tk.Tk()
# Création de l'instance de la classe Application en passant root comme argument master
app = Application(master=root)
app.run()               

