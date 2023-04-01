from queue import Queue, LifoQueue

class CubePuzzle:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.moves = {
            (0,1): "move cube {} from espacement {} to espacement {}",
            (0,2): "move cube {} from espacement {} to espacement {}",
            (1,0): "move cube {} from espacement {} to espacement {}",
            (1,2): "move cube {} from espacement {} to espacement {}",
            (2,0): "move cube {} from espacement {} to espacement {}",
            (2,1): "move cube {} from espacement {} to espacement {}"
        }

    def successors(self, state):
        for i, p1 in enumerate(state):
            for j, p2 in enumerate(state):
                if i != j and len(p1) > 0:
                    if len(p2) == 0 or p1[-1] < p2[-1]:
                        new_state = [list(p) for p in state]
                        #print("Before move: ", new_state)
                        new_state[j].append(new_state[i].pop())
                        #print("After move: ", new_state)
                        yield new_state, self.moves[(i, j)].format(new_state[j][-1], i, j)


    def bfs(self):
        visited = set()
        q = Queue()
        q.put((self.start, []))
        while not q.empty():
            state, path = q.get()
            if state == self.goal:
                return path
            if tuple(map(tuple, state)) not in visited:
                visited.add(tuple(map(tuple, state)))
                for new_state, move in self.successors(state):
                    q.put((new_state, path + [move]))
        return None

    def dfs(self):
        visited = set()
        q = LifoQueue()
        q.put((self.start, []))
        while not q.empty():
            state, path = q.get()
            if state == self.goal:
                return path
            if tuple(map(tuple, state)) not in visited:
                visited.add(tuple(map(tuple, state)))
                for new_state, move in self.successors(state):
                    q.put((new_state, path + [move]))
        return None


# Demander à l'utilisateur de remplir les états initial et final
start = []
print("==== donner l'etat initial ====")
for i in range(3):
    pole = []
    while True:
        cube = input("Entrez un cube pour l'espacement {} (ou 'fini' pour arrêter) : ".format(i))
        if cube == "fini":
            break
        pole.append(int(cube))
    start.append(pole)
print("===============================")
print(start)
print("===============================")


goal = []
print("=== donner l'etat final ===")

for i in range(3):
    pole = []
    while True:
        cube = input("Entrez un cube pour l'espacement {} (ou 'fini' pour arrêter) : ".format(i))
        if cube == "fini":
            break
        pole.append(int(cube))
    goal.append(pole)
print("===============================")
print(goal)
print("===============================")

# Créer l'objet CubePuzzle et effectuer la recherche en BFS et DFS
puzzle = CubePuzzle(start, goal)


print("=== Recherche en BFS ===")
path_bfs = puzzle.bfs()
if path_bfs:
    print("Chemin trouvé en BFS :")
    for move in path_bfs:
        print(move)
else:
    print("Aucune solution trouvée en BFS.")

print("\n=== Recherche en DFS ===")
path_dfs = puzzle.dfs()
if path_dfs:
    print("Chemin trouvé en DFS :")
    for move in path_dfs:
        print(move)
else:
    print("Aucune solution trouvée en DFS.")
