# Primiti intr-un fisier text o gramatica si intr-un alt fisier o lista de cuvinte.
# Trebuie sa generati un cod care atunci cand este rulat, va parsa cel de-al doilea
# fisier si va indica daca este corect din punct de vedere sintactic. De exemplu
# scrieti un fisier in Python, care atunci cand primeste o gramatica, scrie intr-un
# fisier rdp.c cod de C cu tot cu main, il compileaza, si atunci cand este rulat,
# parseaza al doilea fisier.(Nu trebuie sa fie tot c, poate sa fie python sau cpp)

tokens = (
    ('->', 'ARROW'),
    ('|', 'OR'),
    ('\n', 'NEW_LINE')
)

# Read file and grammar
grammar = open('gramatica', 'r')
grammar_data = []
i = 0

for line in grammar:
    grammar_data.append(line)
    i += 1

# Array of all productions
print(grammar_data)