import copy
def minimax(board, depth, is_maximizing):
    # Condition d'arrêt
    score = evaluate(board)
    if score is not None or is_board_full(board):
        return score

    # Si c'est le tour du joueur, on cherche à maximiser le score
    if is_maximizing:
        best_score = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'x'
                    score = minimax(board, depth-1, False)
                    board[i][j] = '-'
                    best_score = max(score, best_score)
        return best_score

    # Sinon, c'est le tour de l'adversaire, on cherche à minimiser le score
    else:
        best_score = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'o'
                    score = minimax(board, depth-1, True)
                    board[i][j] = '-'
                    best_score = min(score, best_score)
        return best_score


def find_best_move(board):
    best_score = -1000
    best_move = ()
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = 'x'
                score = minimax(board, 5, False)
                board[i][j] = '-'
                if score is not None and score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move



def evaluate(board):
    # Vérification des lignes
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == 'x':
                return 1
            elif board[i][0] == 'o':
                return -1

    # Vérification des colonnes
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == 'x':
                return 1
            elif board[0][j] == 'o':
                return -1

    # Vérification des diagonales
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'x':
            return 1
        elif board[0][0] == 'o':
            return -1
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 'x':
            return 1
        elif board[0][2] == 'o':
            return -1

    # Match nul
    if is_board_full(board):
        return 0

    # Le jeu n'est pas fini
    return None


def is_board_full(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                return False
    return True


def print_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                print(' ', end=' ')
            else:
                print(board[i][j], end=' ')
            if j != 2:
                print('|', end=' ')
        print()
        if i != 2:
            print('-' * 9)

        
board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

print("========= Bienvenue dans le jeu XO! ===========\n")

while not is_board_full(board):
    print_board(board)
    row = int(input("Entrez le numéro de ligne (0, 1 ou 2): "))
    col = int(input("Entrez le numéro de colonne (0, 1 ou 2): "))

    if board[row][col] != '-':
        print("La case est déjà occupée. <<<<Réessayez.>>>>\n")
        continue

    board[row][col] = 'o'

    if evaluate(board) == -1:
        print_board(board)
        print("Vous avez gagné!!!!!!!!\n")
        break

    if is_board_full(board):
        print_board(board)
        print("Match nul!\n")
        break

    print("L'ordinateur réfléchit...")
    row, col = find_best_move(copy.deepcopy(board))
    board[row][col] = 'x'

    if evaluate(board) == 1:
        print_board(board)
        print("L'ordinateur a gagné!!!!!!!\n")
        break

print("========== Fin du jeu. =============")