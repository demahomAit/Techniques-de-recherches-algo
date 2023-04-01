class Reine:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def est_en_conflit(self, autre_reine):
        return (self.x == autre_reine.x or
                self.y == autre_reine.y or
                self.x + self.y == autre_reine.x + autre_reine.y or
                self.x - self.y == autre_reine.x - autre_reine.y)


class Echiquier:
    def __init__(self):
        self.taille = 8
        self.reines = []

    def placer_reine(self, reine):
        self.reines.append(reine)

    def echiquier_valide(self):
        for i in range(len(self.reines)):
            for j in range(i + 1, len(self.reines)):
                if self.reines[i].est_en_conflit(self.reines[j]):
                    return False
        return True


def dfs_solve(echiquier):
    pile = [echiquier]
    while pile:
        etat_actuel = pile.pop()
        if len(etat_actuel.reines) == etat_actuel.taille:
            return etat_actuel
        for y in range(etat_actuel.taille):
            nouvelle_reine = Reine(len(etat_actuel.reines), y)
            nouveau_echiquier = Echiquier()
            nouveau_echiquier.reines = list(etat_actuel.reines)
            nouveau_echiquier.placer_reine(nouvelle_reine)
            if nouveau_echiquier.echiquier_valide():
                pile.append(nouveau_echiquier)


def bfs_solve(echiquier):
    file = [echiquier]
    while file:
        etat_actuel = file.pop(0)
        if len(etat_actuel.reines) == etat_actuel.taille:
            return etat_actuel
        for y in range(etat_actuel.taille):
            nouvelle_reine = Reine(len(etat_actuel.reines), y)
            nouveau_echiquier = Echiquier()
            nouveau_echiquier.reines = list(etat_actuel.reines)
            nouveau_echiquier.placer_reine(nouvelle_reine)
            if nouveau_echiquier.echiquier_valide():
                file.append(nouveau_echiquier)
    return None


def main():
    echiquier_initial = Echiquier()
    solution_dfs = dfs_solve(echiquier_initial)
    solution_bfs = bfs_solve(echiquier_initial)

    if solution_dfs is not None:
        print("Solution trouvée en utilisant l'algorithme de recherche en profondeur:")
        for reine in solution_dfs.reines:
            print("({}, {})".format(reine.x, reine.y))
    else:
        print("Pas de solution trouvée en utilisant l'algorithme de recherche en profondeur.")

    if solution_bfs is not None:
        print("Solution trouvée en utilisant l'algorithme de recherche en largeur:")
        for reine in solution_bfs.reines:
            print("({}, {})".format(reine.x, reine.y))
    else:
        print("Pas de solution trouvée en utilisant l'algorithme de recherche en largeur.")


if __name__ == '__main__':
    main()
