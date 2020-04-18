import numpy as np

OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
OR = '|'
KLEENE_STAR = '*'
CONCATENATE = '.'
END_SIGN = '#'
LAMBDA = '$'  # using $ for lambda values

SPECIAL_SIGNS = [OPEN_BRACKET, CLOSE_BRACKET, OR, KLEENE_STAR]


class Node:
    def __init__(self, value, pos=None):
        self.value = value
        self.right_child = None
        self.left_child = None
        # used for printing statements
        self.level = 0
        self.position = pos
        self.first_pos = None
        self.last_pos = None
        self.follow_pos = None
        self.is_lambda = False

    def set_node_data(self):
        self.set_pos()
        self.set_is_lambda()
        # update last_pos and first_pos in case of lambda children
        self.set_pos()

    def set_is_lambda(self):
        if self.value in [KLEENE_STAR, LAMBDA]:
            self.is_lambda = True
        elif self.value is OR:
            self.is_lambda = self.left_child.is_lambda or self.right_child.is_lambda
        elif self.value is CONCATENATE:
            self.is_lambda = self.left_child.is_lambda and self.right_child.is_lambda

    def set_right_child(self, child):
        self.right_child = child

    def set_left_child(self, child):
        self.left_child = child

    def is_operator(self):
        if self.value in [KLEENE_STAR, CONCATENATE, OR]:
            return True
        return False

    def __str__(self):
        print('Is Lambda : ' + str(self.is_lambda))
        print(self.first_pos, end=" ")
        print('(' + self.value + ')', end=" ")
        print(self.last_pos)
        if self.left_child is not None:
            print('Left child : (' + self.left_child.value + ')')
        if self.right_child is not None:
            print('Right child : (' + self.right_child.value + ')')
        return self.value

    def __repr__(self):
        return self.value

    # set First_Pos and Last_pos for every type of node in the tree
    def set_pos(self):
        if self.is_operator():
            if self.value == CONCATENATE:
                self.first_pos = self.left_child.first_pos
                self.last_pos = self.right_child.last_pos

                # Checking for lambda children

                if self.left_child.is_lambda:
                    if self.value == CONCATENATE:
                        self.first_pos = np.concatenate((self.first_pos, self.right_child.first_pos), axis=0)
                if self.right_child.is_lambda:
                    if self.value == CONCATENATE:
                        self.last_pos = np.concatenate((self.last_pos, self.left_child.last_pos), axis=0)

            elif self.value == KLEENE_STAR:
                self.first_pos = self.left_child.first_pos
                self.last_pos = self.left_child.last_pos

            else:
                # OR operator
                self.first_pos = np.concatenate((self.left_child.first_pos, self.right_child.first_pos), axis=0)
                self.last_pos = np.concatenate((self.left_child.last_pos, self.right_child.last_pos), axis=0)

        elif self.is_lambda:
            # for lambda values set the first and last pos as empty sets
            self.first_pos = np.array([])
            self.last_pos = np.array([])
        else:
            self.first_pos = np.array([self.position])
            self.last_pos = np.array([self.position])
