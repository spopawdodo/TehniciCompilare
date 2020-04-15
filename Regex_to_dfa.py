# Define constants
import numpy as np

OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
OR = '|'
KLEENE_STAR = '*'
CONCATENATE = '.'
END_SIGN = '#'

SPECIAL_SIGNS = [OPEN_BRACKET, CLOSE_BRACKET, OR, KLEENE_STAR]
OPERATOR_PRECEDENCE = {OR:2, KLEENE_STAR:1, CONCATENATE:2}


class Stack:
    def __init__(self):
        self.size = 0
        self.content = list()

    def is_empty(self):
        return not bool(self.content)

    def push(self, elem):
        self.content.append(elem)
        self.size = len(self.content) #- 1

    def pop_(self):
        if not self.is_empty():
            elem = self.content.pop()
            self.size = len(self.content) - 1
            return elem
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.content[-1]
        else:
            return None

    def display(self):
        if not self.is_empty():
            return self.content
        else:
            return None


def infix_to_postfix(entry):
    changer = Stack()
    new_exp = list()
    for k in entry:
        if k.isalpha() or k is END_SIGN:
            new_exp.append(k)
        elif k in [KLEENE_STAR, OR, CONCATENATE]:
            prec_check = OPERATOR_PRECEDENCE[k]
            while True:
                curr_op = changer.peek()
                if curr_op in [KLEENE_STAR, OR, CONCATENATE]:
                    curr_op_val = OPERATOR_PRECEDENCE[curr_op]
                    if curr_op_val <= prec_check:
                        add = changer.pop_()
                        new_exp.append(add)
                    else:
                        break
                else:
                    break
            changer.push(k)
        elif k == OPEN_BRACKET:
            changer.push(k)
        elif k == CLOSE_BRACKET:
            while True:
                if changer.peek() == OPEN_BRACKET:
                    changer.pop_()
                    break
                else:
                    add = changer.pop_()
                    new_exp.append(add)
    return new_exp


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


class Node:
    def __init__(self, value, pos=None):
        self.value = value
        self.parent = None
        self.right_child = None
        self.left_child = None
        self.level = 0
        self.position = pos
        self.first_pos = None
        self.last_pos = None
        self.follow_pos = None

    def set_parent(self, parent):
        if parent.is_operator:
            self.parent = parent
        else:
            print("ERROR: Parent must be operator! "+parent.value+' received')

    def set_right_child(self, child):
        self.right_child = child

    def set_left_child(self, child):
        self.left_child = child

    def is_operator(self):
        if self.value in [KLEENE_STAR, CONCATENATE, OR]:
            return True
        return False

    def display(self):
        print(self.first_pos)
        print(self.value)
        print(self.last_pos)
        if self.left_child is not None:
            print(self.left_child.value, end=" ")
        if self.right_child is not None:
            print(self.right_child.value, end=" ")

    def set_pos(self):
        if self.is_operator():
            if self.value == CONCATENATE:
                self.first_pos = self.left_child.first_pos
                self.last_pos = self.right_child.last_pos
            elif self.value == KLEENE_STAR:
                self.first_pos = self.left_child.first_pos
                self.last_pos = self.left_child.last_pos
            else:
                # OR operator
                #self.first_pos = self.left_child.first_pos
                self.first_pos = np.concatenate((self.left_child.first_pos, self.right_child.first_pos), axis=0)
                #self.last_pos = self.left_child.last_pos
                self.last_pos = np.concatenate((self.left_child.last_pos, self.right_child.last_pos), axis=0)
        else:
            self.first_pos = np.array([self.position])
            self.last_pos = np.array([self.position])


class RegexTree:
    def __init__(self, root, length):
        self.stack = []
        self.root = root
        self.number_of_nodes = length

    def display(self):
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

            print(s.first_pos, end = "")
            print(s.last_pos, end ="")
            print('('+s.value+')\t\t', end = "")

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            if s.left_child is not None:
                s.left_child.level = s.level + 1
                queue.append(s.left_child)
                next_print += '|\t\t'
            else :
                next_print += '\t\t'

            if s.right_child is not None:
                s.right_child.level = s.level + 1
                queue.append(s.right_child)
                next_print += '\ \t\t'
            else:
                next_print += '\t\t'

    def convert_to_DFA(self):

        return DFA

#class DeterministFiniteAutomata:



def create_regex_tree(infix_regex):
    stack = Stack()
    pos = 0

    for c in infix_regex:
        if c.isalpha() or c is END_SIGN:
            node = Node(c, pos)
            node.set_pos()
            stack.push(node)
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
            node.set_pos()
            stack.push(node)
        elif c is KLEENE_STAR:
            # operator with 1 child node
            node = Node(c)

            if stack.peek() is None:
                print('ERROR: No child nodes available')
                exit()

            node.set_left_child(stack.pop_())
            node.set_pos()
            stack.push(node)

        else:
            print('ERROR: Untreated character '+ c)
            exit()

    if stack.size is not 1:
        print('Error in parsing the string, there are ' + str(stack.size) + 'nodes')
        exit()

    return RegexTree(stack.pop_(), len(regex))


# Read regular expression
file = open('regex', 'r')

regex = file.read()
check_brackets(regex)
regex = infix_to_postfix(regex)
print(regex)
# ['a', 'b', '|', '*', 'a', 'a', '.', 'b', '|', '.']
# regex_1 = '((((a|b)*).((a.a)|b)).#)'
regex_tree = create_regex_tree(regex)
regex_tree.display()
