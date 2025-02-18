class Tile:
    """
    A class to represent a tile on the Minesweeper board.

    Attributes
    ----------
    x : int
        The x-coordinate of the tile.
    y : int
        The y-coordinate of the tile.
    revealed : bool
        Whether the tile has been revealed.
    is_mine : bool
        Whether the tile is a mine.
    neighbor_mines : int
        The number of mines in neighboring tiles.
    flagged : bool
        Whether the tile has been flagged.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.is_mine = False
        self.neighbor_mines = 0
        self.flagged = False