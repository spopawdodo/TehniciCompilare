# Define constants
from Regex_To_Dfa.infixToPostfix import infix_to_postfix, is_char, Stack
from Regex_To_Dfa.node import Node
from Regex_To_Dfa.regexTree import RegexTree
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
OR = '|'
KLEENE_STAR = '*'
CONCATENATE = '.'
END_SIGN = '#'
LAMBDA = '$'  # using $ for lambda values

SPECIAL_SIGNS = [OPEN_BRACKET, CLOSE_BRACKET, OR, KLEENE_STAR]

follow_pos_table = {}


def check_brackets(regex):
    stack = []
    for c in regex:
        if c == OPEN_BRACKET:
            stack.append('.')
        if c == CLOSE_BRACKET:
            if len(stack) == 0:
                exit('No opening brackets found')
            stack.pop()
    if len(stack) == 0:
        return True
    exit('No closing brackets found')


def update_follow_pos(node, follow_pos):
    if node in follow_pos_table:
        follow_pos_table[node] = np.concatenate((follow_pos_table[node], follow_pos), axis=0)
    else:
        follow_pos_table[node] = follow_pos


def create_regex_tree(infix_regex):
    stack = Stack()
    pos = 0
    node_pos = {}

    for c in infix_regex:
        if is_char(c):
            node = Node(c, pos)
            node.set_node_data()
            node_pos[pos] = node
            stack.push(node)
            if c is END_SIGN:
                update_follow_pos(pos, np.array([]))
            pos += 1
        elif c in [OR, CONCATENATE]:
            # operators with 2 children
            node = Node(c)
            if stack.peek() is None:
                print('ERROR: No child nodes available')
                exit()

            node.set_right_child(stack.pop_())

            if stack.peek() is None:
                print('ERROR: No child nodes available')
                exit()

            node.set_left_child(stack.pop_())
            node.set_node_data()

            # Setting follow_pos
            if node.value == CONCATENATE:
                for i in node.left_child.last_pos:
                    update_follow_pos(i, node.right_child.first_pos)

            stack.push(node)
        elif c is KLEENE_STAR:
            # operator with 1 child node
            node = Node(c)

            if stack.peek() is None:
                print('ERROR: No child nodes available')
                exit()

            node.set_left_child(stack.pop_())
            node.set_node_data()

            # Setting follow_pos
            for i in node.left_child.last_pos:
                update_follow_pos(i, node.left_child.first_pos)

            stack.push(node)

        else:
            print('ERROR: Untreated character '+ c)
            exit()

    if stack.size is not 1:
        print('Error in parsing the string, there are ' + str(stack.size) + 'nodes')
        exit()

    return RegexTree(stack.pop_(), len(regex), node_pos, follow_pos_table)


# Read regular expression

# regex_1 = '((((a|b)*).((a.a)|b)).#)'
# ['a', 'b', '|', '*', 'a', 'a', '.', 'b', '|', '.']

regex = '(((((a.b)|a)*).(((a|$).b)*)).#)'
file = open('Regex_To_Dfa/regex', 'r')

regex = file.read()
check_brackets(regex)
regex = infix_to_postfix(regex)
#print(regex)

regex_tree = create_regex_tree(regex)
dfa = regex_tree.convert_to_dfa()
print(dfa)
dfa.check_word(dfa.q0, ['a', 'b', 'b', '#'])
dfa.check_word(dfa.q0, ['b', '#'])
dfa.check_word(dfa.q0, ['#'])

G = nx.MultiDiGraph()

for state in dfa.Q:
    print(state.number)
    G.add_node(state.number)

G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
G.graph['graph'] = {'scale': '3'}

for transition in dfa.Transitions:
    #G.add_weighted_edges_from([(transition.first_state.number, transition.second_state.number, transition.input)])
    G.add_edge(transition.first_state.number, transition.second_state.number)

A = to_agraph(G)
A.layout('dot')
A.draw('multi.png')

