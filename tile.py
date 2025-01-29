class tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.isMine = False
        self.neighborMines = 0
        self.flagged = False