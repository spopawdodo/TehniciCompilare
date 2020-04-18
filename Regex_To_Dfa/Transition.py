class Transition:
    def __init__(self, first_state, input, second_state):
        self.first_state = first_state
        self.input = input
        self.second_state = second_state

    def __str__(self):
        return str(self.first_state) + ' goes with input ' + self.input + ' to state ' + str(self.second_state) + '\n'

    def __repr__(self):
        return str(self.first_state) + ' goes with input ' + self.input + ' to state ' + str(self.second_state) + '\n'
