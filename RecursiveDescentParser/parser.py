
with open("gramatica") as f:
    grammar = f.readlines()
grammar = [gr.replace("\n", "") for gr in grammar]

gr_list = []
gr_nonterminal_tokens = []
for gr in grammar:
    gr_split = gr.split("->")
    assert len(
        gr_split) == 2, "Cannot be parsed. The token -> needs to be present as a delimiter instead got: {}".format(gr)

    gr_str = gr_split[1].replace(" ", "")
    gr_nonterminal = gr_split[0].replace(" ", "")

    gr_list.append([gr_nonterminal, gr_str])
    gr_nonterminal_tokens.append(gr_nonterminal)

parser_f = open("gen_parser.py", 'w')

# Add exception handling
# Add file opening(read the words for testing)
# Match function : cam match more than one char at a time and returns the remaining string
headers = f"""
import os

class ParsingException(Exception):
    def __init__(self, message):
        super(ParsingException, self).__init__(message)

input_f = None
with open("input") as f:
    input_f = f.readlines()

def match(input_str, match_str):
    if match_str == input_str[:len(match_str)]:
        return input_str[len(match_str):]
    else:
        raise ParsingException("'%s' not matched in input '%s'" % (match_str, input_str))
"""
parser_f.write(headers)

# gr_list = [['S', 'aAb|bC|fDgguDg|Eh|F'], ['A', 'aA|b'],...]
gr_dict = {non_terminal: rules for non_terminal, rules in gr_list}

for nonterminal_name, gr_rules in gr_list:
    if nonterminal_name == 'S':
        # first production
        rule_arr = []
        for gr_rule in gr_rules.split("|"):
            if gr_rule[0] in gr_nonterminal_tokens:
                # if the first character is a nonTerminal we have to check the first character from next nonTerminal
                gr_r = gr_dict[gr_rule[0]]
                # we use ! as a way of knowing which rules were generated in this way
                # S -> A | B; if A -> b C | c and B -> a B | c
                # so a rule like that becomes S -> b A ! | a B !
                rule_arr.extend([gr_r[0] + gr_rule + "!"])
            else:
                rule_arr.append(gr_rule)

        gr_rules = '|'.join(rule_arr)

    # write recursive function to file
    recurse_functions = f"""
def {nonterminal_name}(input_str):"""

    # gr_rules = 'aAb|bC|fDgguDg|Eh|F' in case nonterminal_name is S
    for rule in gr_rules.split("|"):
        recurse_functions += f"""
    if input_str[0] == '{rule[0]}':"""

        # no non-terminal => directly match string and return the remaining input string
        nonterminal_token_indices = [i for i, x in enumerate(rule) if x in gr_nonterminal_tokens]
        if not nonterminal_token_indices:
            if len(rule) == 1:
                recurse_functions += f"""
        return input_str[1:]"""
            elif len(rule) >= 2:
                recurse_functions += f"""
        res = match(input_str, '{rule}')
        return res"""
            continue

        # production also contains non-terminals
        rules = rule
        for sp_token in gr_nonterminal_tokens:
            # replace non-terminals with '|'
            rules = rules.replace(sp_token, "|")

        rules = rules.split("|")
        rules_tokens = [[r, rule[nt_idx]] for r, nt_idx in zip(rules, nonterminal_token_indices)]
        # if rule == 'aAb'
        # rules = ['a', 'b']
        # rules_tokens = [['a', 'A']]
        if len(rules_tokens) != len(rules):
            # there are rules without any non-terminal token, so we add them to the rules_token
            # in order to have all the rules in the list formatted correctly
            if rules[len(rules_tokens):] != ['']:
                rules_tokens.append(rules[len(rules_tokens):])

        # rules_tokens = [['a', 'A'], ['b']]
        for rt in rules_tokens:
            if len(rt) == 1:
                # a rule only with terminal token
                if len(rt[0]) == 1:
                    if rt[0] != '':
                        recurse_functions += f"""
        if 'res' in locals():
            res = match(res, '{rt[0]}')
        else:
            res = match(input_str, '{rt[0]}')
            """
            elif len(rt) == 2:
                nont_token = rt[1]
                # a rule with non-terminal token
                if len(rt[0]) == 1:
                    # handling the special case S -> A | B
                    # S -> bA! | aB!
                    if '!' in rules_tokens[-1][-1]:
                        rules_tokens[-1][-1] = rules_tokens[-1][-1].replace("!", "")
                        recurse_functions += f"""
        if 'res' in locals():
            res = {nont_token}(res)
        else:
            res = {nont_token}(input_str)
            """
                    else:
                        # only one string before the non-terminal token, ex: a A
                        # base case
                        recurse_functions += f"""
        if 'res' in locals():
            res = {nont_token}(res[1:])
        else:
            res = {nont_token}(input_str[1:])
            """
                elif len(rt[0]) >= 2:
                    # more than one character before the nonterminal token, ex: a b A
                    recurse_functions += f"""
        if 'res' in locals():
            res = match(res, '{rt[0][:-1]}')
        else:
            res = match(input_str, '{rt[0][:-1]}')
        match(res, '{rt[0][-1]}')
        res = {nont_token}(res[1:])
            """

        # for S check if the remaining string is empty
        if nonterminal_name == 'S':
            recurse_functions += f"""
        if len(res) == 0:
            return True
        raise ParsingException("The last '%s' not matched in input '%s'" % (res, input_str))
        """
        else:
            recurse_functions += f"""
        return res
        """
    # string not matched case
    recurse_functions += f"""
    else:
        raise ParsingException("No rule matched")
"""

    parser_f.write(recurse_functions)

# main code
end_function = f"""
for in_f in input_f:
    in_f = in_f.replace("\\n\", "")
    try:
        {gr_list[0][0]}(in_f)
        print("Input %s parsed correctly" % in_f)
    except ParsingException as e:
        print("Input %s cannot be parsed: %s" % (in_f, e))
"""
parser_f.write(end_function)
