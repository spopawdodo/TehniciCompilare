import numpy as np

class DFA:

    def __init__(self):
        self.Q = {}
        self.E = set()
        self.Transitions = {}
        self.q0 = None
        self.F = set()

    def __str__(self):
        print(self.Transitions)
        return 'Q : ' + str(self.Q) + '\nE : ' + str(self.E) + '\nq0 :' + str(self.q0) + '\nF: ' + str(self.F) + '\n'

    def __repr__(self):
        print(self.Transitions)
        return 'Q : ' + str(self.Q) + '\nE : ' + str(self.E) + '\nq0 :' + str(self.q0) + '\nF: ' + str(self.F) + '\n'

    def check(self, word):
        return self.check_word(self.q0, list(word))

    def check_word(self, state, word):
        if state.final and word == ['#']:
            print('Word belongs to DFA')
            return True
        elif word == '#' and not state.final:
            return False

        char = word.pop(0)
        if char not in self.E:
            print('Character not recognized by DFA : ' + char)
            return False

        has_next_state = False
        for transition in self.Transitions:
            if transition.first_state == state and transition.input == char:
                has_next_state = True
                self.check_word(transition.second_state, word)

        if not has_next_state:
            print('Word not recognized by DFA')
            return False






