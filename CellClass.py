
class CellClass:
    def __init__(self, value, posX, posY, ListNeighbourValue):
        self.value = 0
        self.posX = posX
        self.posY = posY
        self.LNV = ListNeighbourValue

    def update(self):
        count = 0
        for value in self.LNV:
            count += value

        if count == 3: #Dead cell with 3 live neighbours becomes alive/live cell with 3 stays alive
            self.value = 1

        if count == 2 and self.value = 1: #Any live cell with two live neighbours lives on to the next generation.
            self.value = 1

        else: #all other cases the cell dies
            self.value == 0

        return

    def getValue(self):
        return self.value
