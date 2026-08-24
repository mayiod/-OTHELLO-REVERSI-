"""
PROYECTO 1 - FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (UNAB)
Juego: Othello (Reversi)
Entrega 1: Modo Humano vs Humano con tablero parametrizable (n x n, n par >= 4)
"""

# Constantes de representacion
PLAYER_A = 'A'
PLAYER_B = 'B'
EMPTY = '.'

# Ocho direcciones posibles: (delta_fila, delta_columna)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


class OthelloGame:
    """Clase encargada de modelar el estado y las reglas de Othello."""

    def __init__(self, n: int = 8):
        if n < 4 or n % 2 != 0:
            raise ValueError("El tamaño del tablero debe ser un numero par mayor o igual a 4.")
        self.n = n
        self.board = [[EMPTY for _ in range(n)] for _ in range(n)]
        self.current_player = PLAYER_A
        self.consecutive_passes = 0
        self._init_board()

    def _init_board(self):
        """
        Ubica las fichas iniciales segun la especificacion:
        m = n // 2
        A en (m, m) y (m+1, m+1) [base 1] -> [m-1][m-1] y [m][m] [base 0]
        B en (m, m+1) y (m+1, m) [base 1] -> [m-1][m] y [m][m-1] [base 0]
        """
        m = self.n // 2
        self.board[m - 1][m - 1] = PLAYER_A
        self.board[m][m] = PLAYER_A
        self.board[m - 1][m] = PLAYER_B
        self.board[m][m - 1] = PLAYER_B

    def get_opponent(self, player: str) -> str:
        """Retorna el jugador contrario."""
        return PLAYER_B if player == PLAYER_A else PLAYER_A

    def is_inside(self, r: int, c: int) -> bool:
        """Verifica si las coordenadas (r, c) pertenecen al tablero."""
        return 0 <= r < self.n and 0 <= c < self.n

    def get_flips_in_direction(self, r: int, c: int, dr: int, dc: int, player: str) -> list:
        """
        Encuentra las fichas a voltear en una direccion especifica (dr, dc).
        Requiere 1 o mas fichas rivales consecutivas delimitadas por una ficha propia.
        """
        opponent = self.get_opponent(player)
        flips = []
        curr_r = r + dr
        curr_c = c + dc

        while self.is_inside(curr_r, curr_c) and self.board[curr_r][curr_c] == opponent:
            flips.append((curr_r, curr_c))
            curr_r += dr
            curr_c += dc

        if self.is_inside(curr_r, curr_c) and self.board[curr_r][curr_c] == player:
            return flips
        return []

    def get_valid_flips(self, r: int, c: int, player: str) -> list:
        """Retorna la lista de todas las casillas que se voltean al colocar en (r, c)."""
        if not self.is_inside(r, c) or self.board[r][c] != EMPTY:
            return []

        total_flips = []
        for dr, dc in DIRECTIONS:
            flips = self.get_flips_in_direction(r, c, dr, dc, player)
            total_flips.extend(flips)
        return total_flips

    def get_valid_moves(self, player: str) -> dict:
        """Retorna un diccionario {(r, c): [fichas_a_voltear]} con los movimientos validos."""
        moves = {}
        for r in range(self.n):
            for c in range(self.n):
                flips = self.get_valid_flips(r, c, player)
                if flips:
                    moves[(r, c)] = flips
        return moves

    def make_move(self, r: int, c: int) -> bool:
        """
        Ejecuta la jugada en (r, c) para el jugador actual.
        Voltea las piezas correspondientes y cede el turno.
        """
        flips = self.get_valid_flips(r, c, self.current_player)
        if not flips:
            return False

        self.board[r][c] = self.current_player
        for fr, fc in flips:
            self.board[fr][fc] = self.current_player

        self.consecutive_passes = 0
        self.current_player = self.get_opponent(self.current_player)
        return True

    def pass_turn(self):
        """Pasa el turno cuando no hay jugadas legales disponibles."""
        self.consecutive_passes += 1
        self.current_player = self.get_opponent(self.current_player)

    def is_game_over(self) -> bool:
        """
        Determina si el juego finalizo por:
        1. Dos pases consecutivos.
        2. Ningun jugador tiene jugadas posibles (incluye tablero lleno).
        """
        if self.consecutive_passes >= 2:
            return True
        moves_a = len(self.get_valid_moves(PLAYER_A))
        moves_b = len(self.get_valid_moves(PLAYER_B))
        return moves_a == 0 and moves_b == 0

    def get_scores(self) -> dict:
        """Cuenta el total de fichas de cada jugador."""
        scores = {PLAYER_A: 0, PLAYER_B: 0}
        for r in range(self.n):
            for c in range(self.n):
                cell = self.board[r][c]
                if cell in scores:
                    scores[cell] += 1
        return scores


def print_board(game:OthelloGame):
    """muestra el tablero en consola con numeracion base 1 y casillas marcadas(?)."""
    valid_moves = game.get_valid_moves(game.current_player).keys()

    header = "    " + " ".join(f"{c + 1:2}" for c in range(game.n))
    print("\n" + header)
    print("   +" + "---" * game.n + "+")

    for r in range(game.n):
        row_str = f"{r + 1:2} |"
        for c in range(game.n):
            if (r, c) in valid_moves:
                row_str += "  x" # Casilla valida 
            else:
                cell = game.board[r][c]
                if cell == PLAYER_A:
                    row_str += " ⚫" # Ficha Jugador A
                elif cell == PLAYER_B:
                    row_str += " ⚪" # Ficha Jugador B
                else:
                    row_str += "  ." # Casilla vacia
        row_str += " |"
        print(row_str)

    print("   +" + "---" * game.n + "+")
    scores = game.get_scores()
    print(f"Marcador -> Jugador A ⚫: {scores[PLAYER_A]} | Jugador B ⚪: {scores[PLAYER_B]}")




#tamaño del tablero
def ask_board_size() -> int:
    """Solicita y valida el tamaño n del tablero por consola."""
    while True:
        try:
            val = input("Ingrese tamaño de tablero n (par >= 4, defecto 4): ").strip()
            if val == "":
                return 4
            n = int(val)
            if n >= 4 and n % 2 == 0:
                return n
            print("Error: El tamaño debe ser un numero par mayor o igual a 4.")
        except ValueError:
            print("Error: Debe ingresar un valor numerico entero.")


def play_game():
    """Bucle principal de la partida Humano vs Humano."""
    print("=" * 45)
    print("      PROYECTO 1: OTHELLO (REVERSI) - HUMANO VS HUMANO")
    print("=" * 45)

    n = ask_board_size()
    game = OthelloGame(n=n)

    while not game.is_game_over():
        print_board(game)
        valid_moves = game.get_valid_moves(game.current_player)

        # Regla: Paso forzado si no existen jugadas legales
        if not valid_moves:
            print(f"\n[!] El Jugador {game.current_player} no tiene jugadas legales. Pasa turno.")
            input("Presione ENTER para continuar...")
            game.pass_turn()
            continue

        print(f"\nTurno del Jugador: {game.current_player}")
        try:
            entry = input("Ingrese jugada como 'fila columna' o '(Y X)': ").strip().split()
            if len(entry) != 2:
                print("Error: Debe ingresar exactamente dos numeros separados por un espacio.")
                continue

            r = int(entry[0]) - 1
            c = int(entry[1]) - 1

            if not game.make_move(r, c):
                print("Error: Movimiento no valido. Debe elegir una casilla 'x' que encierre fichas rivales.")
        except ValueError:
            print("Error: Formato invalido. Ingrese solo numeros enteros.")

    # Fin de la partida
    print_board(game)
    scores = game.get_scores()
    print("\n" + "=" * 45)
    print("               PARTIDA TERMINADA")
    print("=" * 45)
    print(f"Puntaje Final -> Jugador A: {scores[PLAYER_A]} | Jugador B: {scores[PLAYER_B]}")
    
    if scores[PLAYER_A] > scores[PLAYER_B]:
        print("¡Victoria del Jugador A!")
        return PLAYER_A
    elif scores[PLAYER_B] > scores[PLAYER_A]:
        print("¡Victoria del Jugador B!")
        return PLAYER_B
    else:
        print("¡Empate!")
        return "EMPATE"

def main_menu():
    """Menú principal que mantiene el historial de victorias en la sesión actual."""
    wins_a = 0
    wins_b = 0
    draws = 0

    while True:
        resultado = play_game()
        
        # Actualizar contadores
        if resultado == PLAYER_A:
            wins_a += 1
        elif resultado == PLAYER_B:
            wins_b += 1
        else:
            draws += 1

        # Mostrar estadísticas globales
        print("\n" + "=" * 45)
        print("         ESTADÍSTICAS DE LA SESIÓN")
        print("=" * 45)
        print(f"Victorias Jugador A ⚫ : {wins_a}")
        print(f"Victorias Jugador B ⚪ : {wins_b}")
        print(f"Empates                : {draws}")
        print(f"Total de partidas      : {wins_a + wins_b + draws}")
        print("=" * 45)

        # Preguntar si desean seguir jugando
        resp = input("\n¿Desean jugar otra partida? (s/n): ").strip().lower()
        if resp != 's':
            print("¡Gracias por jugar! Cerrando el programa...")
            break


if __name__ == "__main__":
    main_menu()
