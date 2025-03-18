class Player:

    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color

        self.x = 0
        self.y = 0

        self.score = 1
        self.game = None

    def win(self):
        self.score += 1

    def lose(self):
        self.score -= 1