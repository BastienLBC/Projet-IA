def generate_key(x, y, ennemy_x, ennemy_y, matrix, board, action):
    """Genère une clé unique pour l'état/action.

    Cette fonction sert d'index dans la Q-table pour permettre à l'IA de
    retrouver la valeur associée à un couple (état, action).
    """
    return f"{x},{y},{ennemy_x},{ennemy_y},{matrix},{board},{action}"
