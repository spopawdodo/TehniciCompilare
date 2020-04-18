from Regex_To_Dfa.Determinist_Finite_Automaton import DFA
from Regex_To_Dfa.State import State
from Regex_To_Dfa.Transition import Transition
import numpy as np

OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
OR = '|'
KLEENE_STAR = '*'
CONCATENATE = '.'
END_SIGN = '#'
LAMBDA = '$'  # using $ for lambda values

SPECIAL_SIGNS = [OPEN_BRACKET, CLOSE_BRACKET, OR, KLEENE_STAR]


class RegexTree:
    def __init__(self, root, length, node_pos, follow_pos):
        self.stack = []
        self.root = root
        self.number_of_nodes = length
        self.node_pos = node_pos
        self.follow_pos = follow_pos

    def __str__(self):
        # Breadth First Search
        # Create a queue for BFS
        queue = []
        level = 0

        # Mark the source node as
        # visited and enqueue it
        self.root.level = level
        queue.append(self.root)
        next_print = ''
        while queue:

            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            if s.level is not level:
                print('\n'+next_print)
                next_print = ''
                level += 1
            if s.is_lambda:
                print('T', end=" ")
            else:
                print('F', end=" ")
            print(s.first_pos, end="")
            print(s.last_pos, end="")
            print('('+s.value+')\t\t', end="")

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            if s.left_child is not None:
                s.left_child.level = s.level + 1
                queue.append(s.left_child)
                next_print += '\t|\t\t'
            else:
                next_print += '\t\t\t'

            if s.right_child is not None:
                s.right_child.level = s.level + 1
                queue.append(s.right_child)
                next_print += '\t\ \t\t'
            else:
                next_print += '\t\t\t'

        print()
        print(self.node_pos)
        print(self.follow_pos)
        return ''

    def convert_to_dfa(self):
        dfa = DFA()
        number_of_states = 0

        # set the initial state
        dfa.q0 = State(set(self.follow_pos[0].tolist()), number_of_states)

        if self.root.left_child.is_lambda:
            dfa.q0.final = True

        # add it to the sets of states
        dfa.Q = [dfa.q0]
        number_of_states += 1

        # set the alphabet
        for i in range(len(self.node_pos)):
            if i in self.follow_pos:
                if self.node_pos[i].value not in dfa.E:
                    dfa.E.add(self.node_pos[i].value)

        dfa.Transitions = []

        # Create DFA while visiting it
        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        queue.append(dfa.q0)
        while queue:

            # Dequeue a vertex from queue and print it
            start_state = queue.pop(0)

            if start_state.visited:
                continue

            start_state.visited = True

            # Generate states for all possible transitions
            new_states = {}
            new_transitions = {}
            for i in start_state.pos_set:
                # check if there is already a transition for letter
                if self.node_pos[i].value is END_SIGN:
                    start_state.final = True
                elif self.node_pos[i].value not in new_states.keys():
                    new_states[self.node_pos[i].value] = set(self.follow_pos[i].tolist())
                else:
                    new_states[self.node_pos[i].value].update(self.follow_pos[i].tolist())
            # print(new_states)

            # Convert sets to existing states
            # Or add new states if they don't exist
            for input, state in new_states.items():
                in_set = False

                for s in dfa.Q:
                    if state == s.pos_set:
                        in_set = True
                        new_transitions[input] = s
                        break

                if not in_set:
                    new_state = State(state, number_of_states)
                    number_of_states += 1
                    new_transitions[input] = new_state
                    dfa.Q.append(new_state)
                    queue.append(new_state)

                # add them to transition table
            #print('New Transitions ' + str(new_transitions))

            if start_state == dfa.q0 and self.node_pos[0].value not in new_states.keys():
                new_transitions[self.node_pos[0].value] = start_state

            # Create transitions
            for input, state in new_transitions.items():
                dfa.Transitions.append(Transition(start_state, input, state))

        # add final states
        for state in dfa.Q:
            if state.final:
                dfa.F.add(state)

        return dfa
