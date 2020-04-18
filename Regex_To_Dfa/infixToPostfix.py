# Regex_to_DFA:
#
# convertor from infix to postfix: https://www.codespeedy.com/inter-conversion-of-postfix-and-infix-expression-in-python/
# class Stack and infix_to_postfix(entry)

# added function is_char() so it recognizes the special characters $,#

OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
OR = '|'
KLEENE_STAR = '*'
CONCATENATE = '.'
END_SIGN = '#'
LAMBDA = '$'  # using $ for lambda values

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
        if is_char(k):
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


def is_char(c):
    if c.isalpha() or c in [LAMBDA, END_SIGN]:
        return True
    else:
        return False
