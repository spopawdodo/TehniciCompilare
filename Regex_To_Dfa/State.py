class State:
    def __init__(self, pos_set, number):
        self.pos_set = pos_set
        self.number = number
        self.final = False
        self.visited = False

    def __repr__(self):
        return str(self.number) + ' : ' + str(self.pos_set)

    def __str__(self):
        return str(self.number) + ' : ' + str(self.pos_set)

    def __hash__(self) -> int:
        return super().__hash__()

    def __cmp__(self, other):
        if other == self.pos_set:
            return True
        return False
